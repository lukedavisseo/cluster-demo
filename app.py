# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "polars-lts-cpu",
#     "altair==5.5.0",
# ]
# ///

import marimo

__generated_with = "0.16.1"
app = marimo.App(width="columns")


@app.cell(column=0)
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
    if ".csv" in uploaded_file.name():
        df_embeds_umap = pl.read_csv(uploaded_file.contents())
    else:
        df_embeds_umap = pl.read_parquet(uploaded_file.contents())
    return (df_embeds_umap,)


@app.cell
def _(df_embeds_umap, pl):
    df_embeds_umap_cleaned = (
        df_embeds_umap.filter(
            pl.col('Message').str.len_chars() > 9
        )
    )
    return (df_embeds_umap_cleaned,)


@app.cell
def _(df_embeds_umap_cleaned, mo):
    import altair as alt

    chart = mo.ui.altair_chart(
        alt.Chart(df_embeds_umap_cleaned)
        .mark_point()
        .encode(
            x="x_2d",
            y="y_2d"
        )
        .properties(
            title="Cluster Chart",
            width=1000,
            height=1000
        )
        .configure_title(
            fontSize=20
        )
    )

    chart
    return alt, chart


@app.cell
def _(chart, df_embeds_umap, mo):
    cluster_pc = (chart.value['Message'].len() / df_embeds_umap['Message'].len()) * 100

    mo.vstack(
        [
            mo.md(f"### This cluster accounts for {cluster_pc:.3f}% of the total dataset."),
            chart.value
        ])
    return


@app.cell
def _(mo):
    form = (
        mo.md('''
        **Enter label.**

        {label}
    ''')
        .batch(
            label = mo.ui.text(label="Label")
        )
        .form(clear_on_submit=True, show_clear_button=True)
    )

    form
    return (form,)


@app.cell
def _(chart, form, mo, pl):
    mo.stop(not form.value)

    labelled_df = pl.DataFrame(chart.value).with_columns(
        label=pl.lit(form.value["label"])
    )

    labelled_df
    return


@app.cell(column=1)
def _(mo):
    mo.md(r"""# Labelled Clusters""")
    return


@app.cell
def _(mo):
    uploaded_labelled_file = mo.ui.file(kind="area", multiple=True)
    uploaded_labelled_file
    return (uploaded_labelled_file,)


@app.cell
def _(pl, uploaded_labelled_file):
    uploaded_labelled_file_contents = [contents.contents for contents in uploaded_labelled_file.value]
    csv_files = [pl.scan_csv(csv) for csv in uploaded_labelled_file_contents]
    df_with_labels = pl.concat(csv_files, how="vertical").collect()

    df_with_labels
    return (df_with_labels,)


@app.cell
def _(df_with_labels):
    import random

    colours = [f"#{''.join(random.choices('0123456789ABCDEF', k=6))}" for i in range(df_with_labels['label'].unique().len())]
    return (colours,)


@app.cell
def _(alt, colours, df_with_labels, mo):
    labelled_chart = mo.ui.altair_chart(
        alt.Chart(df_with_labels)
        .mark_point()
        .encode(
            alt.Color('label', 
                  scale=alt.Scale(domain=df_with_labels['label'],
                                  range=colours)),
            x="x_2d",
            y="y_2d"       
        )
        .properties(
            title="Cluster Chart",
            width=1000,
            height=1000
        )
        .configure_title(
            fontSize=20
        )
    )

    labelled_chart
    return


if __name__ == "__main__":
    app.run()
