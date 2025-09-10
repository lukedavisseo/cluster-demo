import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    return mo, pl


@app.cell
def _(mo):
    mo.md(r"""# Cluster Demo""")
    return


@app.cell
def _(mo):
    uploaded_file = mo.ui.file(kind="area")
    uploaded_file
    return (uploaded_file,)


@app.cell
def _(pl, uploaded_file):
    df_embeds_umap = pl.read_parquet(uploaded_file.value[0].contents)
    return (df_embeds_umap,)


@app.cell
def _(df_embeds_umap, mo):
    import altair as alt

    chart = mo.ui.altair_chart(
        alt.Chart(df_embeds_umap)
        .mark_point()
        .encode(
            x="x_2d",
            y="y_2d"
        )
        .properties(
            title="Available Car AI Chat Clusters",
            width=1000,
            height=1000
        )
        .configure_title(
            fontSize=20
        )
    )

    chart
    return (chart,)


@app.cell
def _(chart):
    chart.value
    return


if __name__ == "__main__":
    app.run()
