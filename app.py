import math
import html

import streamlit as st
import pandas as pd
import numpy as np
from google.cloud import bigquery


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Quantacus Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# CSS
# ==========================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #06101c;
    color: #ffffff;
}

.block-container {
    padding-top: 3.2rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    padding-bottom: 3rem;
    max-width: 100%;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ========================================================
   SIDEBAR
======================================================== */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #091522 0%,
        #07111d 100%
    );
    border-right: 1px solid #24364a;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.4rem;
}

section[data-testid="stSidebar"] h2 {
    color: #ffffff !important;
    font-size: 27px !important;
    font-weight: 750 !important;
}

section[data-testid="stSidebar"]
div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

section[data-testid="stSidebar"]
div[role="radiogroup"] label {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 11px;
    padding: 12px 14px;
    min-height: 48px;
}

section[data-testid="stSidebar"]
div[role="radiogroup"] label:hover {
    background-color: #122135;
    border-color: #30465f;
}

section[data-testid="stSidebar"]
div[role="radiogroup"]
label:has(input:checked) {
    background-color: #17283c;
    border-color: #3c5774;
}

section[data-testid="stSidebar"]
input[type="radio"] {
    display: none;
}


/* ========================================================
   HEADER
======================================================== */

.dashboard-title {
    font-size: 30px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.2;
}

.dashboard-subtitle {
    font-size: 14px;
    color: #8e9aac;
    margin-top: 5px;
}


/* ========================================================
   KPI
======================================================== */

div[data-testid="stMetric"] {
    background-color: #111c2b;
    border: 1px solid #334154;
    border-radius: 16px;
    padding: 22px 24px;
    min-height: 145px;
}

div[data-testid="stMetricLabel"] {
    color: #dce3eb !important;
    font-size: 16px !important;
}

div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 34px !important;
    font-weight: 700 !important;
}


/* ========================================================
   SELECT / INPUT
======================================================== */

div[data-baseweb="select"] > div {
    background-color: #0d1725 !important;
    border: 1px solid #334154 !important;
    border-radius: 10px !important;
    min-height: 46px;
}

div[data-baseweb="input"] > div {
    background-color: #0d1725 !important;
    border: 1px solid #334154 !important;
    border-radius: 10px !important;
}

div[data-baseweb="tag"] {
    background-color: #22334a !important;
    color: white !important;
}


/* ========================================================
   BUTTON
======================================================== */

.stButton > button,
.stDownloadButton > button {
    background-color: #0d1725;
    color: white;
    border: 1px solid #334154;
    border-radius: 10px;
    min-height: 46px;
    font-weight: 500;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #162437;
    border-color: #60758e;
    color: white;
}


/* ========================================================
   PRODUCT TOP CONTROLS
======================================================== */

div[data-testid="stDownloadButton"] > button {
    font-size: 13px;
    min-height: 40px;
    padding-top: 5px;
    padding-bottom: 5px;
}


/* ========================================================
   POPOVER
======================================================== */

div[data-testid="stPopover"] > button {
    background-color: #0d1725 !important;
    color: white !important;
    border: 1px solid #334154 !important;
    border-radius: 10px !important;
    min-height: 46px !important;
    width: 100%;
}


/* ========================================================
   CONTAINERS
======================================================== */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #101b2a;
    border: 1px solid #334154 !important;
    border-radius: 16px;
}

div[data-testid="stExpander"] {
    background-color: #101b2a;
    border: 1px solid #334154;
    border-radius: 14px;
}


/* ========================================================
   DATAFRAME
======================================================== */

div[data-testid="stDataFrame"] {
    border: 1px solid #334154;
    border-radius: 14px;
    overflow: hidden;
}


/* ========================================================
   TEXT
======================================================== */

.section-title {
    font-size: 23px;
    font-weight: 650;
    color: white;
    margin-bottom: 12px;
}

.filter-title {
    font-size: 18px;
    font-weight: 650;
    color: white;
    margin-bottom: 8px;
}

.filter-info {
    color: #8997aa;
    font-size: 13px;
    margin-top: 8px;
    margin-bottom: 8px;
}

.classification-title {
    color: white;
    font-size: 18px;
    font-weight: 650;
    padding-top: 31px;
}

.pagination-info {
    color: #8997aa;
    font-size: 13px;
    margin-top: 5px;
    margin-bottom: 5px;
}


/* ========================================================
   PRODUCT TABLE
======================================================== */

.product-table-scroll {
    width: 100%;
    overflow-x: auto;
    overflow-y: visible;
    margin-top: 4px;
    padding-bottom: 5px;
}

.product-table {
    width: 100%;
    min-width: 1150px;
    border-collapse: separate;
    border-spacing: 0;
    background-color: #0d1725;
    border: 1px solid #334154;
    border-radius: 14px;
    font-size: 13px;
}

.product-table th {
    background-color: #162337;
    color: #d9e1eb;
    font-size: 12px;
    font-weight: 650;
    text-align: left;
    padding: 13px 14px;
    white-space: nowrap;
    border-bottom: 1px solid #334154;
}

.product-table td {
    padding: 10px 14px;
    color: #edf1f6;
    border-bottom: 1px solid #243448;
    white-space: nowrap;
    vertical-align: middle;
}

.product-table tr:last-child td {
    border-bottom: none;
}


/* ========================================================
   PRODUCT TOTAL
======================================================== */

.product-aggregate-row {
    background-color: #152337 !important;
    font-weight: 650;
}

.product-aggregate-row td {
    border-top: 1px solid #41546c;
}


/* ========================================================
   BREAKDOWN
======================================================== */

.product-breakdown-row {
    background-color: #0b1522;
}

.product-breakdown-row:hover {
    background-color: #111f31 !important;
}

.product-breakdown-row td {
    color: #c4cfdd;
}

.breakdown-total {
    font-weight: 700;
    color: #ffffff !important;
}

.breakdown-child {
    padding-left: 28px !important;
    color: #aebbc9 !important;
    font-weight: 500;
}


/* ========================================================
   PRODUCT IMAGE
======================================================== */

.product-image-cell {
    width: 68px;
    height: 68px;
    position: relative;
}

.product-thumb {
    width: 62px;
    height: 62px;
    object-fit: contain;
    background-color: white;
    border: 1px solid #334154;
    border-radius: 9px;
    cursor: zoom-in;
}

.product-image-preview {
    display: none;
    position: fixed;

    width: 340px;
    height: 340px;

    object-fit: contain;

    top: 50%;
    left: 50%;

    transform: translate(-50%, -50%);

    background-color: white;

    padding: 12px;

    border-radius: 14px;

    border: 1px solid #53657a;

    box-shadow:
        0 18px 60px
        rgba(0,0,0,0.80);

    z-index: 999999;
}

.product-image-cell:hover
.product-image-preview {
    display: block;
}

</style>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# HELPERS
# ==========================================================

def safe_divide(numerator, denominator):

    if denominator is None:
        return 0

    if pd.isna(denominator):
        return 0

    if denominator == 0:
        return 0

    return numerator / denominator


def format_number(value):

    if pd.isna(value):
        return "0"

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


def format_currency(value):

    if pd.isna(value):
        return "₹0"

    value = float(value)

    if abs(value) >= 10_000_000:
        return f"₹{value / 10_000_000:.2f}Cr"

    if abs(value) >= 100_000:
        return f"₹{value / 100_000:.2f}L"

    if abs(value) >= 1_000:
        return f"₹{value / 1_000:.2f}K"

    return f"₹{value:,.2f}"


# ==========================================================
# METRIC CALCULATION
# ==========================================================

def calculate_metrics(dataframe):

    df = dataframe.copy()


    df["CPM"] = (
        df["Spend"]
        /
        df["Impressions"].replace(
            0,
            np.nan,
        )
        *
        1000
    )


    df["CTR"] = (
        df["Clicks"]
        /
        df["Impressions"].replace(
            0,
            np.nan,
        )
        *
        100
    )


    df["CPC"] = (
        df["Spend"]
        /
        df["Clicks"].replace(
            0,
            np.nan,
        )
    )


    df["CPLC"] = (
        df["Spend"]
        /
        df["Link Clicks"].replace(
            0,
            np.nan,
        )
    )


    df["CPLPV"] = (
        df["Spend"]
        /
        df["Landing Page View"].replace(
            0,
            np.nan,
        )
    )


    df["CPVC"] = (
        df["Spend"]
        /
        df["Content View"].replace(
            0,
            np.nan,
        )
    )


    df["CPATC"] = (
        df["Spend"]
        /
        df["Add To Cart"].replace(
            0,
            np.nan,
        )
    )


    df["CPO"] = (
        df["Spend"]
        /
        df["Purchase"].replace(
            0,
            np.nan,
        )
    )


    # Current CAC proxy
    df["CAC"] = (
        df["Spend"]
        /
        df["Purchase"].replace(
            0,
            np.nan,
        )
    )


    df["ROAS"] = (
        df["Purchase Value"]
        /
        df["Spend"].replace(
            0,
            np.nan,
        )
    )


    df["CVR"] = (
        df["Purchase"]
        /
        df["Clicks"].replace(
            0,
            np.nan,
        )
        *
        100
    )


    df["AOV"] = (
        df["Purchase Value"]
        /
        df["Purchase"].replace(
            0,
            np.nan,
        )
    )


    return (
        df
        .replace(
            [
                np.inf,
                -np.inf,
            ],
            np.nan,
        )
        .fillna(0)
    )


def metric_state_key(metric):

    return (
        "product_metric_"
        +
        metric
        .lower()
        .replace(
            " ",
            "_",
        )
    )


def format_metric(metric, value):

    currency_metrics = [
        "Spend",
        "Purchase Value",
        "CPM",
        "CPC",
        "CPLC",
        "CPLPV",
        "CPVC",
        "CPATC",
        "CPO",
        "CAC",
        "AOV",
    ]


    percentage_metrics = [
        "CTR",
        "CVR",
    ]


    count_metrics = [
        "Impressions",
        "Clicks",
        "Link Clicks",
        "Landing Page View",
        "Content View",
        "Add To Cart",
        "Purchase",
        "Products with Click",
        "Products with Impression",
        "Products with Spend",
        "Total Products",
    ]


    if metric in currency_metrics:
        return format_currency(value)


    if metric in percentage_metrics:
        return f"{float(value):.2f}%"


    if metric == "ROAS":
        return f"{float(value):.2f}x"


    if metric in count_metrics:
        return format_number(value)


    return str(value)


def show_dynamic_table(
    dataframe,
    row_height=42,
    max_height=680,
):

    rows = len(dataframe)

    height = (
        42
        +
        rows * row_height
        +
        6
    )

    height = min(
        height,
        max_height,
    )

    height = max(
        height,
        100,
    )

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
        height=height,
        row_height=row_height,
    )


# ==========================================================
# PRODUCT HTML TABLE
# ==========================================================

def render_product_table(
    dataframe,
    breakdown_column,
    metric_columns,
):

    headers = [
        "Product ID",
        "Image",
        "Product Type",
        "Brand",
    ]


    if breakdown_column:

        headers.append(
            breakdown_column
        )


    headers += metric_columns


    header_html = "".join(
        f"<th>{html.escape(str(column))}</th>"
        for column in headers
    )


    rows_html = ""


    for _, row in dataframe.iterrows():

        row_type = row.get(
            "_row_type",
            "aggregate",
        )


        # ==================================================
        # PRODUCT TOTAL
        # ==================================================

        if row_type == "aggregate":

            row_class = (
                "product-aggregate-row"
            )


            product_id = html.escape(
                str(
                    row.get(
                        "Product ID",
                        "",
                    )
                )
            )


            product_type = html.escape(
                str(
                    row.get(
                        "Product Type",
                        "",
                    )
                )
            )


            brand = html.escape(
                str(
                    row.get(
                        "Brand",
                        "",
                    )
                )
            )


            image_url = row.get(
                "Image",
                "",
            )


            if pd.isna(image_url):

                image_url = ""


            image_url = str(
                image_url
            ).strip()


            if image_url:

                safe_url = html.escape(
                    image_url,
                    quote=True,
                )


                image_html = (
                    '<div class="product-image-cell">'

                    f'<img '
                    f'class="product-thumb" '
                    f'src="{safe_url}" '
                    f'loading="lazy">'

                    f'<img '
                    f'class="product-image-preview" '
                    f'src="{safe_url}">'

                    '</div>'
                )

            else:

                image_html = "—"


            if breakdown_column:

                breakdown_html = (
                    '<td class="breakdown-total">'
                    'Total'
                    '</td>'
                )

            else:

                breakdown_html = ""


        # ==================================================
        # CHILD ROW
        # ==================================================

        else:

            row_class = (
                "product-breakdown-row"
            )


            product_id = ""

            product_type = ""

            brand = ""

            image_html = ""


            breakdown_value = row.get(
                breakdown_column,
                "",
            )


            if pd.isna(
                breakdown_value
            ):

                breakdown_value = ""


            breakdown_html = (
                '<td class="breakdown-child">'
                '↳ '
                +
                html.escape(
                    str(
                        breakdown_value
                    )
                )
                +
                '</td>'
            )


        # ==================================================
        # METRIC CELLS
        # ==================================================

        metric_cells = ""


        for metric in metric_columns:

            value = row.get(
                metric,
                0,
            )


            metric_cells += (
                "<td>"
                +
                html.escape(
                    format_metric(
                        metric,
                        value,
                    )
                )
                +
                "</td>"
            )


        rows_html += (
            f'<tr class="{row_class}">'

            f"<td>{product_id}</td>"

            f"<td>{image_html}</td>"

            f"<td>{product_type}</td>"

            f"<td>{brand}</td>"

            f"{breakdown_html}"

            f"{metric_cells}"

            "</tr>"
        )


    st.markdown(
        f"""
<div class="product-table-scroll">

<table class="product-table">

<thead>
<tr>
{header_html}
</tr>
</thead>

<tbody>
{rows_html}
</tbody>

</table>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# LOAD DATA FROM BIGQUERY
# ==========================================================

# PROJECT_ID = "newme-in"
# DASHBOARD_TABLE = "newme-in.en_meta.dashboard_table"


# @st.cache_data(ttl=900)
# def load_data():

#     client = bigquery.Client(
#         project=PROJECT_ID
#     )

#     query = f"""
#     SELECT *
#     FROM `{DASHBOARD_TABLE}`
#     """

#     df = (
#         client
#         .query(query)
#         .to_dataframe()
#     )

# ==========================================================
# LOAD DATA FROM CSV
# ==========================================================

CSV_FILE = "dashboard_data.csv"


@st.cache_data(ttl=900)
def load_data():

    df = pd.read_csv(
        CSV_FILE,
        low_memory=False
    )

    # ======================================================
    # NORMALIZE COLUMN NAMES
    # ======================================================

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(
            " ",
            "_",
            regex=False,
        )
    )

    # ======================================================
    # ALIASES
    # ======================================================

    rename_map = {}

    if (
        "spend" in df.columns
        and
        "spends" not in df.columns
    ):
        rename_map["spend"] = "spends"

    if (
        "adset_id" in df.columns
        and
        "parent_meta_asset_id" not in df.columns
    ):
        rename_map["adset_id"] = "parent_meta_asset_id"

    if (
        "ad_id" in df.columns
        and
        "meta_asset_id" not in df.columns
    ):
        rename_map["ad_id"] = "meta_asset_id"

    if rename_map:
        df = df.rename(columns=rename_map)

    # ======================================================
    # STRING COLUMNS
    # ======================================================

    string_columns = [
        "campaign_id",
        "campaign_name",
        "meta_asset_id",
        "ad_name",
        "parent_meta_asset_id",
        "adset_name",
        "product_id",
        "product_type",
        "brand",
        "image_link",
        "price_bucket",
    ]

    for column in string_columns:
        if column in df.columns:
            df[column] = df[column].astype("string")

    # ======================================================
    # DATE
    # ======================================================

    if "performance_date" in df.columns:
        df["performance_date"] = pd.to_datetime(
            df["performance_date"],
            errors="coerce",
        )

    # ======================================================
    # NUMERIC
    # ======================================================

    numeric_columns = [
        "impressions",
        "clicks",
        "spends",
        "purchase",
        "purchase_value",
        "view_content",
        "add_to_cart",
        "link_clicks",
        "landing_page_view",
        "final_price",
        "sale_price",
        "price",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = (
                pd.to_numeric(
                    df[column],
                    errors="coerce",
                )
                .fillna(0)
            )

    return df
    # ======================================================
    # NORMALIZE COLUMN NAMES
    # ======================================================

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(
            " ",
            "_",
            regex=False,
        )
    )


    # ======================================================
    # ALIASES
    # ======================================================

    rename_map = {}


    if (
        "spend" in df.columns
        and
        "spends" not in df.columns
    ):

        rename_map[
            "spend"
        ] = "spends"


    if (
        "adset_id" in df.columns
        and
        "parent_meta_asset_id"
        not in df.columns
    ):

        rename_map[
            "adset_id"
        ] = (
            "parent_meta_asset_id"
        )


    if (
        "ad_id" in df.columns
        and
        "meta_asset_id"
        not in df.columns
    ):

        rename_map[
            "ad_id"
        ] = (
            "meta_asset_id"
        )


    if rename_map:

        df = df.rename(
            columns=rename_map
        )


    # ======================================================
    # STRING
    # ======================================================

    string_columns = [
        "campaign_id",
        "campaign_name",
        "meta_asset_id",
        "ad_name",
        "parent_meta_asset_id",
        "adset_name",
        "product_id",
        "product_type",
        "brand",
        "image_link",
    ]


    for column in string_columns:

        if column in df.columns:

            df[
                column
            ] = (
                df[
                    column
                ]
                .astype(
                    "string"
                )
            )


    # ======================================================
    # DATE
    # ======================================================

    if (
        "performance_date"
        in df.columns
    ):

        df[
            "performance_date"
        ] = pd.to_datetime(
            df[
                "performance_date"
            ],
            errors="coerce",
        )


    # ======================================================
    # NUMERIC
    # ======================================================

    numeric_columns = [
        "impressions",
        "clicks",
        "spends",
        "purchase",
        "purchase_value",
        "view_content",
        "add_to_cart",
        "link_clicks",
        "landing_page_view",
        "final_price",
        "final_cpo_index",
    ]


    for column in numeric_columns:

        if column in df.columns:

            df[
                column
            ] = (
                pd.to_numeric(
                    df[
                        column
                    ],
                    errors="coerce",
                )
                .fillna(0)
            )


    return df


try:

    df = load_data()

except Exception as error:

    st.error(
        "Unable to load dashboard data from BigQuery."
    )

    st.exception(error)

    st.stop()


if df.empty:

    st.error(
        "dashboard_table currently has no data."
    )

    st.stop()


# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

required_columns = [
    "performance_date",
    "campaign_name",
    "adset_name",
    "ad_name",
    "product_id",
    "product_type",
    "brand",
    "image_link",
    "impressions",
    "clicks",
    "spends",
    "purchase",
    "purchase_value",
    "view_content",
    "add_to_cart",
    "link_clicks",
    "landing_page_view",
]


missing_columns = [
    column
    for column
    in required_columns
    if column
    not in df.columns
]


if missing_columns:

    st.error(
        "Missing columns: "
        +
        ", ".join(
            missing_columns
        )
    )


    st.code(
        "\n".join(
            df.columns.tolist()
        )
    )


    st.stop()


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        "## QScale"
    )


    st.caption(
        "Quantacus Performance"
    )


    st.markdown(
        "---"
    )


    page = st.radio(
        "Navigation",
        options=[
            "📊 Overview",
            "🛍️ Product View",
            "📋 Third View",
        ],
        index=0,
        label_visibility="collapsed",
    )


    st.markdown(
        "---"
    )


    st.caption(
        "Meta Performance Analytics"
    )


# ==========================================================
# DATE LIMITS
# ==========================================================

max_date = (
    df[
        "performance_date"
    ]
    .max()
)


min_date = (
    df[
        "performance_date"
    ]
    .min()
)


if (
    pd.isna(
        max_date
    )
    or
    pd.isna(
        min_date
    )
):

    st.error(
        "No valid performance dates found."
    )

    st.stop()


max_date = (
    max_date.normalize()
)

min_date = (
    min_date.normalize()
)


# ==========================================================
# HEADER
# ==========================================================

(
    title_col,
    spacer_col,
    date_col,
    refresh_col,
) = st.columns(
    [
        4.7,
        2.5,
        2.4,
        1.2,
    ]
)


with title_col:

    st.markdown(
        """
<div class="dashboard-title">
Quantacus Performance
</div>

<div class="dashboard-subtitle">
Meta Ads Performance Dashboard
</div>
""",
        unsafe_allow_html=True,
    )


custom_dates = None


with date_col:

    date_filter = (
        st.selectbox(
            "Date",
            [
                "This month",
                "Last 7 days",
                "Last 14 days",
                "Last 30 days",
                "All time",
                "Custom",
            ],
            label_visibility="collapsed",
            key="global_date_filter",
        )
    )


    if (
        date_filter
        ==
        "Custom"
    ):

        custom_dates = (
            st.date_input(
                "Custom range",
                value=(
                    min_date.date(),
                    max_date.date(),
                ),
                min_value=(
                    min_date.date()
                ),
                max_value=(
                    max_date.date()
                ),
            )
        )


with refresh_col:

    if st.button(
        "↻ Refresh",
        use_container_width=True,
    ):

        st.cache_data.clear()

        st.rerun()


# ==========================================================
# DATE FILTER
# ==========================================================

if (
    date_filter
    ==
    "This month"
):

    start_date = (
        max_date.replace(
            day=1
        )
    )

    end_date = max_date


elif (
    date_filter
    ==
    "Last 7 days"
):

    start_date = (
        max_date
        -
        pd.Timedelta(
            days=6
        )
    )

    end_date = max_date


elif (
    date_filter
    ==
    "Last 14 days"
):

    start_date = (
        max_date
        -
        pd.Timedelta(
            days=13
        )
    )

    end_date = max_date


elif (
    date_filter
    ==
    "Last 30 days"
):

    start_date = (
        max_date
        -
        pd.Timedelta(
            days=29
        )
    )

    end_date = max_date


elif (
    date_filter
    ==
    "All time"
):

    start_date = min_date

    end_date = max_date


else:

    if (
        custom_dates is not None
        and
        len(
            custom_dates
        ) == 2
    ):

        start_date = (
            pd.Timestamp(
                custom_dates[0]
            )
        )

        end_date = (
            pd.Timestamp(
                custom_dates[1]
            )
        )

    else:

        start_date = min_date

        end_date = max_date


date_df = df[
    (
        df[
            "performance_date"
        ]
        >=
        start_date
    )
    &
    (
        df[
            "performance_date"
        ]
        <=
        end_date
    )
].copy()


# ==========================================================
# OVERVIEW
# ==========================================================

if (
    page
    ==
    "📊 Overview"
):

    # ======================================================
    # KPI
    # ======================================================

    spend = (
        date_df[
            "spends"
        ].sum()
    )


    impressions = (
        date_df[
            "impressions"
        ].sum()
    )


    clicks = (
        date_df[
            "clicks"
        ].sum()
    )


    purchase = (
        date_df[
            "purchase"
        ].sum()
    )


    purchase_value = (
        date_df[
            "purchase_value"
        ].sum()
    )


    cpm = safe_divide(
        spend * 1000,
        impressions,
    )


    cpc = safe_divide(
        spend,
        clicks,
    )


    ctr = safe_divide(
        clicks * 100,
        impressions,
    )


    cpo = safe_divide(
        spend,
        purchase,
    )


    cvr = safe_divide(
        purchase * 100,
        clicks,
    )


    row1 = st.columns(
        5
    )


    row1[0].metric(
        "💳 Spend",
        format_currency(
            spend
        ),
    )


    row1[1].metric(
        "👁 Impressions",
        format_number(
            impressions
        ),
    )


    row1[2].metric(
        "🖱 Clicks",
        format_number(
            clicks
        ),
    )


    row1[3].metric(
        "✅ Purchase",
        format_number(
            purchase
        ),
    )


    row1[4].metric(
        "🧾 Purchase Value",
        format_currency(
            purchase_value
        ),
    )


    row2 = st.columns(
        5
    )


    row2[0].metric(
        "📢 CPM",
        format_currency(
            cpm
        ),
    )


    row2[1].metric(
        "💰 CPC",
        format_currency(
            cpc
        ),
    )


    row2[2].metric(
        "🎯 CTR",
        f"{ctr:.2f}%",
    )


    row2[3].metric(
        "🛒 CPO",
        format_currency(
            cpo
        ),
    )


    row2[4].metric(
        "📊 CVR",
        f"{cvr:.2f}%",
    )


    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )


    # ======================================================
    # FILTERS
    # ======================================================

    overview_df = (
        date_df.copy()
    )


    with st.container(
        border=True
    ):

        st.markdown(
            """
<div class="filter-title">
Filters
</div>
""",
            unsafe_allow_html=True,
        )


        (
            campaign_filter_col,
            adset_filter_col,
            ad_filter_col,
            type_filter_col,
        ) = st.columns(
            4
        )


        with campaign_filter_col:

            campaigns = sorted(
                overview_df[
                    "campaign_name"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            selected_campaigns = (
                st.multiselect(
                    "Campaign",
                    options=campaigns,
                    default=[],
                    placeholder="All Campaigns",
                    key="overview_campaign_filter",
                )
            )


        if selected_campaigns:

            overview_df = (
                overview_df[
                    overview_df[
                        "campaign_name"
                    ]
                    .astype(str)
                    .isin(
                        selected_campaigns
                    )
                ]
                .copy()
            )


        with adset_filter_col:

            adsets = sorted(
                overview_df[
                    "adset_name"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            selected_adsets = (
                st.multiselect(
                    "Adset",
                    options=adsets,
                    default=[],
                    placeholder="All Adsets",
                    key="overview_adset_filter",
                )
            )


        if selected_adsets:

            overview_df = (
                overview_df[
                    overview_df[
                        "adset_name"
                    ]
                    .astype(str)
                    .isin(
                        selected_adsets
                    )
                ]
                .copy()
            )


        with ad_filter_col:

            ads = sorted(
                overview_df[
                    "ad_name"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            selected_ads = (
                st.multiselect(
                    "Ad",
                    options=ads,
                    default=[],
                    placeholder="All Ads",
                    key="overview_ad_filter",
                )
            )


        if selected_ads:

            overview_df = (
                overview_df[
                    overview_df[
                        "ad_name"
                    ]
                    .astype(str)
                    .isin(
                        selected_ads
                    )
                ]
                .copy()
            )


        with type_filter_col:

            product_types = sorted(
                overview_df[
                    "product_type"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            selected_product_types = (
                st.multiselect(
                    "Product Type",
                    options=product_types,
                    default=[],
                    placeholder="All Product Types",
                    key="overview_product_type_filter",
                )
            )


        if selected_product_types:

            overview_df = (
                overview_df[
                    overview_df[
                        "product_type"
                    ]
                    .astype(str)
                    .isin(
                        selected_product_types
                    )
                ]
                .copy()
            )


    # ======================================================
    # CLASSIFICATION
    # ======================================================

    with st.container(
        border=True
    ):

        (
            classification_col,
            level1_col,
            level2_col,
            level3_col,
            aggregation_col,
            bucket_col,
        ) = st.columns(
            [
                1.3,
                1.7,
                1.7,
                1.7,
                1.5,
                1.4,
            ]
        )


        with classification_col:

            st.markdown(
                """
<div class="classification-title">
◇ Classification:
</div>
""",
                unsafe_allow_html=True,
            )


        dimensions = [
            "Campaign",
            "Adset",
            "Ad",
            "Product Type",
            "Brand",
            "Price Bucket",
            "Date",
        ]


        with level1_col:

            level_1 = (
                st.selectbox(
                    "Level 1",
                    options=dimensions,
                    index=1,
                    key="overview_level_1",
                )
            )


        level_2_options = [
            dimension
            for dimension
            in dimensions
            if dimension
            !=
            level_1
        ]


        with level2_col:

            level_2 = (
                st.selectbox(
                    "Level 2",
                    options=[
                        "None"
                    ]
                    +
                    level_2_options,
                    key=(
                        f"overview_level_2_"
                        f"{level_1}"
                    ),
                )
            )


        if (
            level_2
            ==
            "None"
        ):

            level_3_options = []

        else:

            level_3_options = [
                dimension
                for dimension
                in dimensions
                if dimension
                not in [
                    level_1,
                    level_2,
                ]
            ]


        with level3_col:

            level_3 = (
                st.selectbox(
                    "Level 3",
                    options=[
                        "None"
                    ]
                    +
                    level_3_options,
                    key=(
                        f"overview_level_3_"
                        f"{level_1}_"
                        f"{level_2}"
                    ),
                )
            )


        with aggregation_col:

            aggregation = (
                st.selectbox(
                    "Aggregation",
                    [
                        "Daily",
                        "Weekly",
                        "Monthly",
                    ],
                    key="overview_aggregation",
                )
            )


        with bucket_col:

            bucket_size = (
                st.number_input(
                    "Bucket Size ₹",
                    min_value=1,
                    value=200,
                    step=50,
                    key="overview_bucket",
                )
            )


    # ======================================================
    # CALCULATED METRICS
    # ======================================================

    with st.container(
        border=True
    ):

        selected_metrics = (
            st.multiselect(
                "Add calculated metrics",
                options=[
                    "CPM",
                    "CTR",
                    "CPC",
                    "CPLC",
                    "CPLPV",
                    "CPVC",
                    "CPATC",
                    "CPO",
                    "ROAS",
                    "CVR",
                    "AOV",
                ],
                default=[],
                placeholder="Select calculated metrics",
                key="overview_metrics",
            )
        )


    # ======================================================
    # CUSTOM METRIC
    # ======================================================

    with st.expander(
        "➕ Add Custom Metric",
        expanded=False,
    ):

        (
            cm1,
            cm2,
            cm3,
            cm4,
        ) = st.columns(
            [
                2,
                2,
                1,
                2,
            ]
        )


        custom_sources = [
            "Spend",
            "Impressions",
            "Clicks",
            "Link Clicks",
            "Landing Page View",
            "Content View",
            "Add To Cart",
            "Purchase",
            "Purchase Value",
            "Products with Click",
            "Products with Impression",
            "Products with Spend",
            "Total Products",
        ]


        with cm1:

            custom_name = (
                st.text_input(
                    "Metric Name",
                    key="overview_custom_name",
                )
            )


        with cm2:

            custom_a = (
                st.selectbox(
                    "Metric A",
                    custom_sources,
                    key="overview_custom_a",
                )
            )


        with cm3:

            custom_operator = (
                st.selectbox(
                    "Operator",
                    [
                        "/",
                        "*",
                        "+",
                        "-",
                    ],
                    key="overview_custom_operator",
                )
            )


        with cm4:

            custom_b = (
                st.selectbox(
                    "Metric B",
                    custom_sources,
                    index=1,
                    key="overview_custom_b",
                )
            )


        cm5, cm6 = st.columns(
            2
        )


        with cm5:

            custom_multiplier = (
                st.selectbox(
                    "Multiply by",
                    [
                        1,
                        100,
                        1000,
                    ],
                    key="overview_custom_multiplier",
                )
            )


        with cm6:

            custom_format = (
                st.selectbox(
                    "Format",
                    [
                        "Number",
                        "Currency",
                        "Percentage",
                    ],
                    key="overview_custom_format",
                )
            )


    # ======================================================
    # PREPARE TABLE
    # ======================================================

    table_df = (
        overview_df.copy()
    )


    table_df[
        "product_id"
    ] = (
        table_df[
            "product_id"
        ]
        .astype(
            "string"
        )
    )


    table_df[
        "_Product_With_Click"
    ] = (
        table_df[
            "product_id"
        ]
        .where(
            table_df[
                "clicks"
            ].fillna(0) > 0
        )
    )


    table_df[
        "_Product_With_Impression"
    ] = (
        table_df[
            "product_id"
        ]
        .where(
            table_df[
                "impressions"
            ].fillna(0) > 0
        )
    )


    table_df[
        "_Product_With_Spend"
    ] = (
        table_df[
            "product_id"
        ]
        .where(
            table_df[
                "spends"
            ].fillna(0) > 0
        )
    )


    table_df[
        "_Campaign"
    ] = (
        table_df[
            "campaign_name"
        ]
        .fillna(
            "Unknown"
        )
        .astype(str)
    )


    if (
        "parent_meta_asset_id"
        in table_df.columns
    ):

        adset_fallback = (
            table_df[
                "parent_meta_asset_id"
            ]
        )

    else:

        adset_fallback = (
            pd.Series(
                "Unknown",
                index=table_df.index,
            )
        )


    table_df[
        "_Adset"
    ] = (
        table_df[
            "adset_name"
        ]
        .fillna(
            adset_fallback
        )
        .fillna(
            "Unknown"
        )
        .astype(str)
    )


    if (
        "meta_asset_id"
        in table_df.columns
    ):

        ad_fallback = (
            table_df[
                "meta_asset_id"
            ]
        )

    else:

        ad_fallback = (
            pd.Series(
                "Unknown",
                index=table_df.index,
            )
        )


    table_df[
        "_Ad"
    ] = (
        table_df[
            "ad_name"
        ]
        .fillna(
            ad_fallback
        )
        .fillna(
            "Unknown"
        )
        .astype(str)
    )


    table_df[
        "_Product Type"
    ] = (
        table_df[
            "product_type"
        ]
        .fillna(
            "Unknown"
        )
        .astype(str)
    )


    table_df[
        "_Brand"
    ] = (
        table_df[
            "brand"
        ]
        .fillna(
            "Unknown"
        )
        .astype(str)
    )


    # ======================================================
    # PRICE BUCKET
    # ======================================================

    if (
        "final_price"
        in table_df.columns
    ):

        final_price = (
            pd.to_numeric(
                table_df[
                    "final_price"
                ],
                errors="coerce",
            )
        )

    else:

        final_price = (
            pd.Series(
                np.nan,
                index=table_df.index,
            )
        )


    bucket_start = (
        np.floor(
            final_price
            /
            bucket_size
        )
        *
        bucket_size
    )


    bucket_end = (
        bucket_start
        +
        bucket_size
    )


    table_df[
        "_Price Bucket"
    ] = np.where(
        final_price.notna(),
        (
            bucket_start
            .fillna(0)
            .astype(int)
            .astype(str)
            +
            "-"
            +
            bucket_end
            .fillna(0)
            .astype(int)
            .astype(str)
        ),
        "Unknown",
    )


    # ======================================================
    # DATE DIMENSION
    # ======================================================

    if (
        aggregation
        ==
        "Daily"
    ):

        table_df[
            "_Date"
        ] = (
            table_df[
                "performance_date"
            ]
            .dt.normalize()
        )


    elif (
        aggregation
        ==
        "Weekly"
    ):

        table_df[
            "_Date"
        ] = (
            table_df[
                "performance_date"
            ]
            -
            pd.to_timedelta(
                table_df[
                    "performance_date"
                ]
                .dt.weekday,
                unit="D",
            )
        ).dt.normalize()


    else:

        table_df[
            "_Date"
        ] = (
            table_df[
                "performance_date"
            ]
            .dt.to_period(
                "M"
            )
            .dt.to_timestamp()
        )


    selected_levels = [
        level_1
    ]


    if (
        level_2
        !=
        "None"
    ):

        selected_levels.append(
            level_2
        )


    if (
        level_3
        !=
        "None"
    ):

        selected_levels.append(
            level_3
        )


    dimension_mapping = {

        "Campaign":
            "_Campaign",

        "Adset":
            "_Adset",

        "Ad":
            "_Ad",

        "Product Type":
            "_Product Type",

        "Brand":
            "_Brand",

        "Price Bucket":
            "_Price Bucket",

        "Date":
            "_Date",

    }


    group_columns = [
        dimension_mapping[
            level
        ]
        for level
        in selected_levels
    ]


    # ======================================================
    # AGGREGATION
    # ======================================================

    summary = (
        table_df

        .groupby(
            group_columns,
            as_index=False,
            dropna=False,
        )

        .agg(

            Spend=(
                "spends",
                "sum",
            ),

            Impressions=(
                "impressions",
                "sum",
            ),

            Clicks=(
                "clicks",
                "sum",
            ),

            Link_Clicks=(
                "link_clicks",
                "sum",
            ),

            Landing_Page_View=(
                "landing_page_view",
                "sum",
            ),

            Content_View=(
                "view_content",
                "sum",
            ),

            Add_To_Cart=(
                "add_to_cart",
                "sum",
            ),

            Purchase=(
                "purchase",
                "sum",
            ),

            Purchase_Value=(
                "purchase_value",
                "sum",
            ),

            Products_With_Click=(
                "_Product_With_Click",
                "nunique",
            ),

            Products_With_Impression=(
                "_Product_With_Impression",
                "nunique",
            ),

            Products_With_Spend=(
                "_Product_With_Spend",
                "nunique",
            ),

            Total_Products=(
                "product_id",
                "nunique",
            ),

        )
    )


    summary.rename(
        columns={

            "_Campaign":
                "Campaign",

            "_Adset":
                "Adset",

            "_Ad":
                "Ad",

            "_Product Type":
                "Product Type",

            "_Brand":
                "Brand",

            "_Price Bucket":
                "Price Bucket",

            "_Date":
                "Date",

            "Link_Clicks":
                "Link Clicks",

            "Landing_Page_View":
                "Landing Page View",

            "Content_View":
                "Content View",

            "Add_To_Cart":
                "Add To Cart",

            "Purchase_Value":
                "Purchase Value",

            "Products_With_Click":
                "Products with Click",

            "Products_With_Impression":
                "Products with Impression",

            "Products_With_Spend":
                "Products with Spend",

            "Total_Products":
                "Total Products",

        },
        inplace=True,
    )


    summary = (
        calculate_metrics(
            summary
        )
    )


    # ======================================================
    # DATE FORMAT
    # ======================================================

    if (
        "Date"
        in summary.columns
    ):

        summary[
            "Date"
        ] = pd.to_datetime(
            summary[
                "Date"
            ]
        )


        if (
            aggregation
            ==
            "Daily"
        ):

            summary[
                "Date"
            ] = (
                summary[
                    "Date"
                ]
                .dt.strftime(
                    "%d %b %Y"
                )
            )


        elif (
            aggregation
            ==
            "Weekly"
        ):

            summary[
                "Date"
            ] = (
                "Week of "
                +
                summary[
                    "Date"
                ]
                .dt.strftime(
                    "%d %b %Y"
                )
            )


        else:

            summary[
                "Date"
            ] = (
                summary[
                    "Date"
                ]
                .dt.strftime(
                    "%b %Y"
                )
            )


    # ======================================================
    # CUSTOM METRIC
    # ======================================================

    custom_active = (
        custom_name.strip()
        !=
        ""
    )


    if custom_active:

        if (
            custom_name
            in summary.columns
        ):

            st.warning(
                "Custom metric name already exists."
            )

            custom_active = False

        else:

            left = (
                summary[
                    custom_a
                ]
            )

            right = (
                summary[
                    custom_b
                ]
            )


            if (
                custom_operator
                ==
                "/"
            ):

                result = (
                    left
                    /
                    right.replace(
                        0,
                        np.nan,
                    )
                )


            elif (
                custom_operator
                ==
                "*"
            ):

                result = (
                    left
                    *
                    right
                )


            elif (
                custom_operator
                ==
                "+"
            ):

                result = (
                    left
                    +
                    right
                )


            else:

                result = (
                    left
                    -
                    right
                )


            summary[
                custom_name
            ] = (
                result
                *
                custom_multiplier
            )


            summary[
                custom_name
            ] = (
                summary[
                    custom_name
                ]
                .replace(
                    [
                        np.inf,
                        -np.inf,
                    ],
                    np.nan,
                )
                .fillna(0)
            )


    # ======================================================
    # SORT
    # ======================================================

    summary = (
        summary
        .sort_values(
            "Spend",
            ascending=False,
        )
        .reset_index(
            drop=True
        )
    )


    base_metrics = [
        "Spend",
        "Impressions",
        "Clicks",
        "Link Clicks",
        "Landing Page View",
        "Content View",
        "Add To Cart",
        "Purchase",
        "Purchase Value",
        "Products with Click",
        "Products with Impression",
        "Products with Spend",
        "Total Products",
    ]


    final_columns = (
        selected_levels
        +
        base_metrics
        +
        selected_metrics
    )


    if custom_active:

        final_columns.append(
            custom_name
        )


    summary = (
        summary[
            final_columns
        ]
    )


    # ======================================================
    # TABLE HEADER
    # ======================================================

    (
        heading_col,
        download_col,
    ) = st.columns(
        [
            8,
            2,
        ]
    )


    with heading_col:

        st.markdown(
            """
<div class="section-title">
Performance Breakdown
</div>
""",
            unsafe_allow_html=True,
        )


    with download_col:

        st.download_button(
            "⬇ Download",
            data=(
                summary
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8"
                )
            ),
            file_name=(
                "performance_breakdown.csv"
            ),
            mime="text/csv",
            use_container_width=True,
        )


    # ======================================================
    # DISPLAY FORMAT
    # ======================================================

    display_df = (
        summary.copy()
    )


    for column in display_df.columns:

        if (
            column
            in
            base_metrics
            +
            selected_metrics
        ):

            display_df[
                column
            ] = (
                display_df[
                    column
                ]
                .apply(
                    lambda value,
                    metric=column:
                    format_metric(
                        metric,
                        value,
                    )
                )
            )


    if custom_active:

        if (
            custom_format
            ==
            "Currency"
        ):

            display_df[
                custom_name
            ] = (
                display_df[
                    custom_name
                ]
                .apply(
                    format_currency
                )
            )


        elif (
            custom_format
            ==
            "Percentage"
        ):

            display_df[
                custom_name
            ] = (
                display_df[
                    custom_name
                ]
                .apply(
                    lambda x:
                    f"{x:.2f}%"
                )
            )


        else:

            display_df[
                custom_name
            ] = (
                display_df[
                    custom_name
                ]
                .apply(
                    lambda x:
                    f"{x:,.2f}"
                )
            )


    show_dynamic_table(
        display_df
    )


    st.caption(
        f"Rows: {len(display_df):,}"
        f" • Last available data: "
        f"{max_date.strftime('%d %b %Y')}"
    )


# ==========================================================
# PRODUCT VIEW
# ==========================================================

elif (
    page
    ==
    "🛍️ Product View"
):

    st.markdown(
        """
<div class="section-title">
Product Performance
</div>
""",
        unsafe_allow_html=True,
    )


    # ======================================================
    # PLACEHOLDER
    #
    # Visually placed above Product Filters.
    # Filled after filtered product count is calculated.
    # ======================================================

    top_product_controls = (
        st.empty()
    )


    product_df = (
        date_df.copy()
    )


    # ======================================================
    # PRODUCT METRICS
    # ======================================================

    product_metric_options = [
        "Impressions",
        "Clicks",
        "Spend",
        "Link Clicks",
        "Landing Page View",
        "Content View",
        "Add To Cart",
        "Purchase",
        "Purchase Value",
        "CPM",
        "CTR",
        "CPC",
        "CPLC",
        "CPLPV",
        "CPVC",
        "CPATC",
        "CPO",
        "CAC",
        "ROAS",
        "CVR",
        "AOV",
    ]


    default_product_metrics = [
        "Impressions",
        "Clicks",
        "Spend",
        "Purchase",
        "Purchase Value",
        "CTR",
        "CPO",
        "ROAS",
    ]


    # ======================================================
    # INITIALIZE METRIC STATE
    # ======================================================

    for metric in (
        product_metric_options
    ):

        state_key = (
            metric_state_key(
                metric
            )
        )


        if (
            state_key
            not in st.session_state
        ):

            st.session_state[
                state_key
            ] = (
                metric
                in default_product_metrics
            )


    # ======================================================
    # PRODUCT FILTERS
    # ======================================================

    with st.container(
        border=True
    ):

        st.markdown(
            """
<div class="filter-title">
Product Filters
</div>
""",
            unsafe_allow_html=True,
        )


        (
            campaign_col,
            adset_col,
            ad_col,
            type_col,
            product_filter_col,
            breakdown_col,
            metrics_col,
        ) = st.columns(
            [
                1.2,
                1.2,
                1.2,
                1.1,
                1.05,
                0.9,
                1.45,
            ]
        )


        # ==================================================
        # CAMPAIGN
        # ==================================================

        with campaign_col:

            campaigns = sorted(
                product_df[
                    "campaign_name"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            selected_campaigns = (
                st.multiselect(
                    "Campaign",
                    options=campaigns,
                    default=[],
                    placeholder="All Campaigns",
                    key="product_campaign_filter",
                )
            )


        if selected_campaigns:

            product_df = (
                product_df[
                    product_df[
                        "campaign_name"
                    ]
                    .astype(str)
                    .isin(
                        selected_campaigns
                    )
                ]
                .copy()
            )


        # ==================================================
        # ADSET
        # ==================================================

        with adset_col:

            adsets = sorted(
                product_df[
                    "adset_name"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            selected_adsets = (
                st.multiselect(
                    "Adset",
                    options=adsets,
                    default=[],
                    placeholder="All Adsets",
                    key="product_adset_filter",
                )
            )


        if selected_adsets:

            product_df = (
                product_df[
                    product_df[
                        "adset_name"
                    ]
                    .astype(str)
                    .isin(
                        selected_adsets
                    )
                ]
                .copy()
            )


        # ==================================================
        # AD
        # ==================================================

        with ad_col:

            ads = sorted(
                product_df[
                    "ad_name"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            selected_ads = (
                st.multiselect(
                    "Ad",
                    options=ads,
                    default=[],
                    placeholder="All Ads",
                    key="product_ad_filter",
                )
            )


        if selected_ads:

            product_df = (
                product_df[
                    product_df[
                        "ad_name"
                    ]
                    .astype(str)
                    .isin(
                        selected_ads
                    )
                ]
                .copy()
            )


        # ==================================================
        # PRODUCT TYPE
        # ==================================================

        with type_col:

            product_types = sorted(
                product_df[
                    "product_type"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            selected_product_types = (
                st.multiselect(
                    "Product Type",
                    options=product_types,
                    default=[],
                    placeholder="All Types",
                    key="product_type_filter",
                )
            )


        if selected_product_types:

            product_df = (
                product_df[
                    product_df[
                        "product_type"
                    ]
                    .astype(str)
                    .isin(
                        selected_product_types
                    )
                ]
                .copy()
            )


        # ==================================================
        # PRODUCT FILTER
        # ==================================================

        with product_filter_col:

            product_filter = (
                st.selectbox(
                    "Product Filter",
                    options=[
                        "All Products",
                        "Purchase > 0",
                        "Purchase = 0",
                        "Spend > 0",
                        "Impressions > 0",
                    ],
                    index=0,
                    key="product_filter",
                )
            )


        # ==================================================
        # BREAKDOWN
        # ==================================================

        with breakdown_col:

            product_breakdown = (
                st.selectbox(
                    "Breakdown",
                    options=[
                        "None",
                        "Campaign",
                        "Adset",
                        "Ad",
                        "Day",
                    ],
                    index=0,
                    key="product_breakdown",
                )
            )


        # ==================================================
        # METRIC DROPDOWN
        # ==================================================

        with metrics_col:

            st.markdown(
                """
<div style="
font-size:14px;
font-weight:500;
margin-bottom:7px;
">
Metrics
</div>
""",
                unsafe_allow_html=True,
            )


            selected_metric_count = len(
                [
                    metric
                    for metric
                    in product_metric_options
                    if st.session_state.get(
                        metric_state_key(
                            metric
                        ),
                        False,
                    )
                ]
            )


            with st.popover(
                f"☑ {selected_metric_count} selected",
                use_container_width=True,
            ):

                st.caption(
                    "Select columns to show"
                )


                (
                    select_all_col,
                    clear_col,
                ) = st.columns(
                    2
                )


                with select_all_col:

                    if st.button(
                        "Select All",
                        key="product_metric_select_all",
                        use_container_width=True,
                    ):

                        for metric in (
                            product_metric_options
                        ):

                            st.session_state[
                                metric_state_key(
                                    metric
                                )
                            ] = True


                        st.rerun()


                with clear_col:

                    if st.button(
                        "Clear",
                        key="product_metric_clear",
                        use_container_width=True,
                    ):

                        for metric in (
                            product_metric_options
                        ):

                            st.session_state[
                                metric_state_key(
                                    metric
                                )
                            ] = False


                        st.rerun()


                st.markdown(
                    "---"
                )


                for metric in (
                    product_metric_options
                ):

                    st.checkbox(
                        metric,
                        key=(
                            metric_state_key(
                                metric
                            )
                        ),
                    )


    # ======================================================
    # SELECTED METRICS
    # ======================================================

    product_metrics = [
        metric
        for metric
        in product_metric_options
        if st.session_state.get(
            metric_state_key(
                metric
            ),
            False,
        )
    ]


    # ======================================================
    # CLEAN DIMENSIONS
    # ======================================================

    for column in [
        "product_type",
        "brand",
        "campaign_name",
        "adset_name",
        "ad_name",
    ]:

        product_df[
            column
        ] = (
            product_df[
                column
            ]
            .fillna(
                "Unknown"
            )
            .astype(str)
        )


    product_df[
        "image_link"
    ] = (
        product_df[
            "image_link"
        ]
        .astype(
            "string"
        )
        .str.strip()
        .replace(
            "",
            pd.NA,
        )
    )


    product_df[
        "_Product_Day"
    ] = (
        product_df[
            "performance_date"
        ]
        .dt.normalize()
    )


    # ======================================================
    # PRODUCT TOTAL
    # ======================================================

    product_totals = (
        product_df

        .groupby(
            [
                "product_id",
                "product_type",
                "brand",
            ],
            as_index=False,
            dropna=False,
        )

        .agg(

            Image=(
                "image_link",
                "first",
            ),

            Spend=(
                "spends",
                "sum",
            ),

            Impressions=(
                "impressions",
                "sum",
            ),

            Clicks=(
                "clicks",
                "sum",
            ),

            Link_Clicks=(
                "link_clicks",
                "sum",
            ),

            Landing_Page_View=(
                "landing_page_view",
                "sum",
            ),

            Content_View=(
                "view_content",
                "sum",
            ),

            Add_To_Cart=(
                "add_to_cart",
                "sum",
            ),

            Purchase=(
                "purchase",
                "sum",
            ),

            Purchase_Value=(
                "purchase_value",
                "sum",
            ),

        )
    )


    product_totals.rename(
        columns={

            "product_id":
                "Product ID",

            "product_type":
                "Product Type",

            "brand":
                "Brand",

            "Link_Clicks":
                "Link Clicks",

            "Landing_Page_View":
                "Landing Page View",

            "Content_View":
                "Content View",

            "Add_To_Cart":
                "Add To Cart",

            "Purchase_Value":
                "Purchase Value",

        },
        inplace=True,
    )


    product_totals[
        "Image"
    ] = (
        product_totals[
            "Image"
        ]
        .fillna("")
    )


    # ======================================================
    # METRICS AFTER AGGREGATION
    # ======================================================

    product_totals = (
        calculate_metrics(
            product_totals
        )
    )


    # ======================================================
    # PRODUCT FILTER
    # ======================================================

    if (
        product_filter
        ==
        "Purchase > 0"
    ):

        product_totals = (
            product_totals[
                product_totals[
                    "Purchase"
                ] > 0
            ]
            .copy()
        )


    elif (
        product_filter
        ==
        "Purchase = 0"
    ):

        product_totals = (
            product_totals[
                product_totals[
                    "Purchase"
                ] == 0
            ]
            .copy()
        )


    elif (
        product_filter
        ==
        "Spend > 0"
    ):

        product_totals = (
            product_totals[
                product_totals[
                    "Spend"
                ] > 0
            ]
            .copy()
        )


    elif (
        product_filter
        ==
        "Impressions > 0"
    ):

        product_totals = (
            product_totals[
                product_totals[
                    "Impressions"
                ] > 0
            ]
            .copy()
        )


    # ======================================================
    # SORT PRODUCTS
    # ======================================================

    product_totals = (
        product_totals
        .sort_values(
            [
                "Purchase",
                "Spend",
            ],
            ascending=[
                False,
                False,
            ],
        )
        .reset_index(
            drop=True
        )
    )


    # ======================================================
    # PAGINATION
    # ======================================================

    PAGE_SIZE = 50


    total_products = len(
        product_totals
    )


    total_pages = max(
        1,
        math.ceil(
            total_products
            /
            PAGE_SIZE
        ),
    )


    page_options = list(
        range(
            1,
            total_pages + 1
        )
    )


    page_key = (
        "product_page_selector"
    )


    if (
        page_key
        in st.session_state
        and
        st.session_state[
            page_key
        ]
        not in page_options
    ):

        st.session_state[
            page_key
        ] = 1


    # ======================================================
    # PAGE + DOWNLOAD
    #
    # Placeholder was created ABOVE Product Filters.
    # ======================================================

    with top_product_controls.container():

        (
            top_space,
            page_col,
            download_col,
        ) = st.columns(
            [
                8.2,
                0.85,
                0.95,
            ]
        )


        with page_col:

            current_page = (
                st.selectbox(
                    "Page",
                    options=page_options,
                    format_func=(
                        lambda page_number:
                        f"{page_number}/{total_pages}"
                    ),
                    label_visibility="collapsed",
                    key=page_key,
                )
            )


        with download_col:

            st.download_button(
                "⬇ Download",
                data=(
                    product_totals
                    .to_csv(
                        index=False
                    )
                    .encode(
                        "utf-8"
                    )
                ),
                file_name=(
                    "product_performance.csv"
                ),
                mime="text/csv",
                use_container_width=True,
            )


    # ======================================================
    # CURRENT PAGE
    # ======================================================

    start_product = (
        current_page - 1
    ) * PAGE_SIZE


    end_product = min(
        start_product
        +
        PAGE_SIZE,
        total_products,
    )


    page_products = (
        product_totals
        .iloc[
            start_product:end_product
        ]
        .copy()
    )


    page_product_ids = (
        page_products[
            "Product ID"
        ]
        .astype(str)
        .tolist()
    )


    # ======================================================
    # NO BREAKDOWN
    # ======================================================

    if (
        product_breakdown
        ==
        "None"
    ):

        display_product_df = (
            page_products.copy()
        )


        display_product_df[
            "_row_type"
        ] = (
            "aggregate"
        )


        display_breakdown = None


    # ======================================================
    # BREAKDOWN
    # ======================================================

    else:

        breakdown_mapping = {

            "Campaign":
                "campaign_name",

            "Adset":
                "adset_name",

            "Ad":
                "ad_name",

            "Day":
                "_Product_Day",

        }


        breakdown_source_column = (
            breakdown_mapping[
                product_breakdown
            ]
        )


        breakdown_source_df = (
            product_df[
                product_df[
                    "product_id"
                ]
                .astype(str)
                .isin(
                    page_product_ids
                )
            ]
            .copy()
        )


        # ==================================================
        # BREAKDOWN AGGREGATION
        # ==================================================

        breakdown_summary = (
            breakdown_source_df

            .groupby(
                [
                    "product_id",
                    breakdown_source_column,
                ],
                as_index=False,
                dropna=False,
            )

            .agg(

                Spend=(
                    "spends",
                    "sum",
                ),

                Impressions=(
                    "impressions",
                    "sum",
                ),

                Clicks=(
                    "clicks",
                    "sum",
                ),

                Link_Clicks=(
                    "link_clicks",
                    "sum",
                ),

                Landing_Page_View=(
                    "landing_page_view",
                    "sum",
                ),

                Content_View=(
                    "view_content",
                    "sum",
                ),

                Add_To_Cart=(
                    "add_to_cart",
                    "sum",
                ),

                Purchase=(
                    "purchase",
                    "sum",
                ),

                Purchase_Value=(
                    "purchase_value",
                    "sum",
                ),

            )
        )


        breakdown_summary.rename(
            columns={

                "product_id":
                    "Product ID",

                breakdown_source_column:
                    product_breakdown,

                "Link_Clicks":
                    "Link Clicks",

                "Landing_Page_View":
                    "Landing Page View",

                "Content_View":
                    "Content View",

                "Add_To_Cart":
                    "Add To Cart",

                "Purchase_Value":
                    "Purchase Value",

            },
            inplace=True,
        )


        # ==================================================
        # METRIC CALCULATION AFTER BREAKDOWN
        # ==================================================

        breakdown_summary = (
            calculate_metrics(
                breakdown_summary
            )
        )


        # ==================================================
        # HIERARCHY
        # ==================================================

        hierarchy_rows = []


        for _, total_row in (
            page_products.iterrows()
        ):

            product_id = str(
                total_row[
                    "Product ID"
                ]
            )


            # ----------------------------------------------
            # TOTAL ROW
            # ----------------------------------------------

            total_record = (
                total_row.to_dict()
            )


            total_record[
                "_row_type"
            ] = (
                "aggregate"
            )


            total_record[
                product_breakdown
            ] = (
                "Total"
            )


            hierarchy_rows.append(
                total_record
            )


            # ----------------------------------------------
            # CHILD ROWS
            # ----------------------------------------------

            children = (
                breakdown_summary[
                    breakdown_summary[
                        "Product ID"
                    ]
                    .astype(str)
                    ==
                    product_id
                ]
                .copy()
            )


            if (
                product_breakdown
                ==
                "Day"
            ):

                children[
                    "_sort_date"
                ] = (
                    pd.to_datetime(
                        children[
                            "Day"
                        ],
                        errors="coerce",
                    )
                )


                children = (
                    children
                    .sort_values(
                        "_sort_date",
                        ascending=False,
                    )
                )


                children[
                    "Day"
                ] = (
                    pd.to_datetime(
                        children[
                            "Day"
                        ],
                        errors="coerce",
                    )
                    .dt.strftime(
                        "%d %b %Y"
                    )
                )


            else:

                children = (
                    children
                    .sort_values(
                        "Spend",
                        ascending=False,
                    )
                )


            for _, child in (
                children.iterrows()
            ):

                child_record = (
                    child.to_dict()
                )


                child_record[
                    "_row_type"
                ] = (
                    "breakdown"
                )


                child_record[
                    "Product Type"
                ] = ""


                child_record[
                    "Brand"
                ] = ""


                child_record[
                    "Image"
                ] = ""


                hierarchy_rows.append(
                    child_record
                )


        display_product_df = (
            pd.DataFrame(
                hierarchy_rows
            )
        )


        display_breakdown = (
            product_breakdown
        )


    # ======================================================
    # PRODUCT TABLE
    # ======================================================

    render_product_table(
        dataframe=display_product_df,
        breakdown_column=(
            display_breakdown
        ),
        metric_columns=(
            product_metrics
        ),
    )


    # ======================================================
    # FOOTER INFO BELOW TABLE
    # ======================================================

    if (
        total_products
        ==
        0
    ):

        footer_text = (
            "No products found"
        )

    else:

        footer_text = (
            f"Products: "
            f"<b>{total_products:,}</b>"

            f"&nbsp;&nbsp;•&nbsp;&nbsp;"

            f"Showing "
            f"<b>{start_product + 1:,}–{end_product:,}</b> "
            f"of "
            f"<b>{total_products:,}</b> products"

            f"&nbsp;&nbsp;•&nbsp;&nbsp;"

            f"{PAGE_SIZE} products per page"
        )


    if (
        product_breakdown
        !=
        "None"
    ):

        footer_text += (
            f"&nbsp;&nbsp;•&nbsp;&nbsp;"
            f"Breakdown: "
            f"<b>{product_breakdown}</b>"
        )


    st.markdown(
        f"""
<div class="pagination-info"
style="
padding: 4px 2px 8px 2px;
">
{footer_text}
</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# THIRD VIEW
# ==========================================================

else:

    st.markdown(
        """
<div class="section-title">
Third View
</div>
""",
        unsafe_allow_html=True,
    )


    st.info(
        "The third view can be added here."
    )