# ============================================================
#  Streaming Platform — Genre Dominance Analysis
#  Tools: Python + MySQL (SQL embedded inline)
#  Libraries: mysql-connector-python, pandas, matplotlib
#
#  Install: pip install mysql-connector-python pandas matplotlib
# ============================================================

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# ── 1. DATABASE CONNECTION ───────────────────────────────────────────────────
# Update these credentials to match your MySQL setup

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="streaming_db"
    )


# ── 2. CREATE TABLE (run once) ───────────────────────────────────────────────
# This creates the catalog table if it doesn't exist yet

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS catalog (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            platform     VARCHAR(20),
            type         VARCHAR(10),
            title        VARCHAR(200),
            genre        VARCHAR(200),
            rating       VARCHAR(10),
            release_year INT,
            duration     VARCHAR(20),
            date_added   DATE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Table ready.")


# ── 3. LOAD CSV DATA INTO MYSQL ──────────────────────────────────────────────
# Reads each platform CSV, tags it with the platform name,
# and inserts every row into MySQL using executemany()

def load_csv_to_mysql(csv_path, platform_name, column_map):
    df = pd.read_csv(csv_path)

    # rename CSV columns to match our table
    df = df.rename(columns=column_map)

    # tag with platform name
    df["platform"] = platform_name

    # keep only the columns our table needs
    cols = ["platform", "type", "title", "genre",
            "rating", "release_year", "duration", "date_added"]

    # only keep columns that exist in this CSV
    df = df[[c for c in cols if c in df.columns]]
    df = df.where(pd.notnull(df), None)  # replace NaN with None for MySQL

    conn = get_connection()
    cursor = conn.cursor()

    # build the INSERT SQL dynamically based on available columns
    placeholders = ", ".join(["%s"] * len(df.columns))
    col_names    = ", ".join(df.columns)

    sql = f"INSERT INTO catalog ({col_names}) VALUES ({placeholders})"

    rows = [tuple(row) for row in df.itertuples(index=False, name=None)]
    cursor.executemany(sql, rows)

    conn.commit()
    print(f"Loaded {cursor.rowcount} rows for {platform_name}.")
    cursor.close()
    conn.close()


# ── 4. FETCH GENRE DATA ──────────────────────────────────────────────────────
# SQL embedded directly in Python as a string.
# Returns a pandas DataFrame ready for analysis.

def fetch_genre_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # SQL query embedded in Python
    # Pulls platform + genre for every non-null row
    sql = """
        SELECT
            platform,
            genre
        FROM catalog
        WHERE genre IS NOT NULL
          AND genre != ''
        ORDER BY platform
    """

    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return pd.DataFrame(rows)


# ── 5. FETCH PLATFORM SUMMARY ────────────────────────────────────────────────
# A second embedded SQL query — total titles and movie/show split per platform

def fetch_platform_summary():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT
            platform,
            COUNT(*)                                              AS total_titles,
            SUM(CASE WHEN type = 'Movie'   THEN 1 ELSE 0 END)   AS movies,
            SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END)   AS tv_shows,
            ROUND(AVG(release_year), 0)                          AS avg_release_year
        FROM catalog
        GROUP BY platform
        ORDER BY total_titles DESC
    """

    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return pd.DataFrame(rows)


# ── 6. CLEAN & EXPLODE GENRES ────────────────────────────────────────────────
# Genres are stored as "Dramas, Romantic Movies" — one string per row.
# .str.split() + .explode() turns each genre into its own row.

def explode_genres(df):
    df = df.copy()
    df["genre"] = df["genre"].str.split(", ")   # "A, B" → ["A", "B"]
    df = df.explode("genre")                     # one row → many rows
    df["genre"] = df["genre"].str.strip()        # remove extra whitespace
    df = df[df["genre"] != ""]                   # drop empty strings
    df = df.dropna(subset=["genre"])
    return df


# ── 7. COUNT & RANK GENRES ───────────────────────────────────────────────────
# Groups by platform + genre, counts titles, keeps top N per platform

def get_top_genres(df, top_n=8):
    counts = (
        df.groupby(["platform", "genre"])
          .size()
          .reset_index(name="count")
          .sort_values("count", ascending=False)
    )
    # keep top N genres per platform
    top = counts.groupby("platform").head(top_n).reset_index(drop=True)
    return counts, top


# ── 8. CHART: HORIZONTAL BAR — one per platform ──────────────────────────────

def plot_bar_charts(top_genres, save_path="genre_bars.png"):
    platforms = top_genres["platform"].unique()
    platform_colors = {
        "Netflix": "#E50914",
        "Disney+": "#113CCF",
        "Hulu":    "#1CE783",
        "Amazon":  "#FF9900",
    }

    fig, axes = plt.subplots(
        1, len(platforms),
        figsize=(6 * len(platforms), 6)
    )

    # if only one platform, axes won't be a list — fix that
    if len(platforms) == 1:
        axes = [axes]

    for ax, platform in zip(axes, platforms):
        data = (
            top_genres[top_genres["platform"] == platform]
            .sort_values("count")            # sort ascending for barh
        )
        color = platform_colors.get(platform, "#888780")
        ax.barh(data["genre"], data["count"], color=color, height=0.6)
        ax.set_title(platform, fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Number of titles")
        ax.tick_params(axis="y", labelsize=10)
        ax.spines[["top", "right"]].set_visible(False)

    fig.suptitle("Top genres per streaming platform", fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Saved → {save_path}")


# ── 9. CHART: HEATMAP — all platforms side by side ───────────────────────────

def plot_heatmap(all_counts, save_path="genre_heatmap.png"):
    # pivot: rows = genres, columns = platforms
    pivot = all_counts.pivot_table(
        index="genre",
        columns="platform",
        values="count",
        fill_value=0
    )

    # sort rows by total count across all platforms
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]
    pivot = pivot.head(20)   # top 20 genres for readability

    fig, ax = plt.subplots(figsize=(8, 10))
    im = ax.imshow(pivot.values, aspect="auto", cmap="YlOrRd")

    # axis labels
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, fontsize=12, fontweight="bold")
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=9)

    # add count values inside each cell
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.values[i, j]
            if val > 0:
                ax.text(j, i, str(int(val)),
                        ha="center", va="center",
                        fontsize=8, color="black")

    plt.colorbar(im, ax=ax, label="Number of titles", shrink=0.6)
    ax.set_title("Genre dominance heatmap — all platforms",
                 fontsize=14, pad=16)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Saved → {save_path}")


# ── 10. PRINT SUMMARY TABLE ──────────────────────────────────────────────────

def print_summary(summary_df):
    print("\n" + "=" * 55)
    print("  PLATFORM SUMMARY")
    print("=" * 55)
    print(summary_df.to_string(index=False))
    print("=" * 55 + "\n")


# ── MAIN — runs everything in order ─────────────────────────────────────────

def main():
    # Step 1: create table (safe to run multiple times)
    create_table()

    # Step 2: load your CSVs — update paths to match your files
    # Comment these out after the first run so you don't duplicate data
    load_csv_to_mysql(
        csv_path="netflix_titles.csv",
        platform_name="Netflix",
        column_map={"listed_in": "genre"}   # Netflix uses "listed_in" for genres
    )
    load_csv_to_mysql(
        csv_path="disney_plus_titles.csv",
        platform_name="Disney+",
        column_map={"listed_in": "genre"}
    )
    load_csv_to_mysql(
        csv_path="hulu_titles.csv",
        platform_name="Hulu",
        column_map={"genres": "genre"}      # Hulu may use "genres"
    )

    # Step 3: fetch and print platform summary (SQL query #1)
    print("Fetching platform summary...")
    summary = fetch_platform_summary()
    print_summary(summary)

    # Step 4: fetch raw genre data (SQL query #2)
    print("Fetching genre data...")
    df = fetch_genre_data()
    print(f"Loaded {len(df)} rows.\n")

    # Step 5: clean and explode genres
    df_exploded = explode_genres(df)

    # Step 6: count and rank
    all_counts, top_genres = get_top_genres(df_exploded, top_n=8)

    # Step 7: plot bar charts
    print("Plotting bar charts...")
    plot_bar_charts(top_genres, save_path="genre_bars.png")

    # Step 8: plot heatmap
    print("Plotting heatmap...")
    plot_heatmap(all_counts, save_path="genre_heatmap.png")

    print("Done! Both charts saved.")


if __name__ == "__main__":
    main()
