
from pathlib import Path
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import (
    Dash,
    dcc,
    html,
    dash_table,
    Input,
    Output
)

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"

# ------------------------------------------------------------
# LOAD SAVED OUTPUTS
# ------------------------------------------------------------

inventory = pd.read_csv(
    OUTPUT_DIR / "inventory_recommendations.csv"
)

forecast = pd.read_csv(
    OUTPUT_DIR / "lightgbm_prediction_intervals.csv"
)

model_results = pd.read_csv(
    OUTPUT_DIR / "final_model_summary.csv"
)

forecast["date"] = pd.to_datetime(
    forecast["date"]
)

inventory["store_id"] = (
    inventory["store_id"]
    .astype(str)
)

forecast["store_id"] = (
    forecast["store_id"]
    .astype(str)
)

stores = sorted(
    inventory["store_id"]
    .unique()
)

store_options = [
    "ALL"
] + stores

# ------------------------------------------------------------
# DASH APP
# ------------------------------------------------------------

app = Dash(__name__)

server = app.server

app.title = (
    "Nationwide Demand Forecasting & Inventory Optimization"
)

CARD_STYLE = {
    "padding": "18px",
    "backgroundColor": "white",
    "border": "1px solid #e2e8f0",
    "borderRadius": "10px",
    "textAlign": "center"
}

# ------------------------------------------------------------
# LAYOUT
# ------------------------------------------------------------

app.layout = html.Div(

    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f8fafc",
        "padding": "24px"
    },

    children=[

        html.H1(
            "Nationwide Demand Forecasting & Inventory Optimization"
        ),

        html.P(
            "M5 Walmart • LightGBM • TFT • OR-Tools",
            style={
                "color": "#64748b",
                "fontSize": "17px"
            }
        ),

        html.Hr(),

        html.Div([

            html.Label(
                "Select Store",
                style={
                    "fontWeight": "bold"
                }
            ),

            dcc.Dropdown(

                id="store-filter",

                options=[
                    {
                        "label":
                            "All Stores"
                            if store == "ALL"
                            else store,

                        "value":
                            store
                    }

                    for store in store_options
                ],

                value="ALL",

                clearable=False
            )

        ],
        style={
            "maxWidth": "350px",
            "marginBottom": "25px"
        }),

        html.Div(

            id="kpi-cards",

            style={
                "display": "grid",
                "gridTemplateColumns":
                    "repeat(auto-fit, minmax(170px, 1fr))",
                "gap": "15px",
                "marginBottom": "25px"
            }
        ),

        html.Div([

            dcc.Graph(
                id="forecast-chart"
            ),

            dcc.Graph(
                id="model-chart"
            )

        ],
        style={
            "display": "grid",
            "gridTemplateColumns":
                "repeat(auto-fit, minmax(420px, 1fr))",
            "gap": "20px"
        }),

        html.Div([

            dcc.Graph(
                id="risk-chart"
            ),

            dcc.Graph(
                id="order-chart"
            )

        ],
        style={
            "display": "grid",
            "gridTemplateColumns":
                "repeat(auto-fit, minmax(420px, 1fr))",
            "gap": "20px"
        }),

        html.H2(
            "Inventory Recommendations"
        ),

        dash_table.DataTable(

            id="inventory-table",

            page_size=15,

            sort_action="native",

            filter_action="native",

            style_table={
                "overflowX": "auto"
            },

            style_cell={
                "textAlign": "center",
                "padding": "8px",
                "fontSize": "12px"
            },

            style_header={
                "fontWeight": "bold",
                "backgroundColor": "#e2e8f0"
            }
        ),

        html.P(
            "Note: inventory balances, supplier lead times and cost "
            "parameters are simulated because they are not included "
            "in the M5 dataset.",
            style={
                "fontSize": "12px",
                "color": "#64748b"
            }
        )
    ]
)

# ------------------------------------------------------------
# CALLBACK
# ------------------------------------------------------------

@app.callback(

    [
        Output("kpi-cards", "children"),
        Output("forecast-chart", "figure"),
        Output("model-chart", "figure"),
        Output("risk-chart", "figure"),
        Output("order-chart", "figure"),
        Output("inventory-table", "data"),
        Output("inventory-table", "columns")
    ],

    Input(
        "store-filter",
        "value"
    )
)

def update_dashboard(selected_store):

    if selected_store == "ALL":

        inv = inventory.copy()

        fc = forecast.copy()

        display_name = "All Stores"

    else:

        inv = inventory[
            inventory["store_id"]
            ==
            selected_store
        ].copy()

        fc = forecast[
            forecast["store_id"]
            ==
            selected_store
        ].copy()

        display_name = selected_store

    # --------------------------------------------------------
    # KPI VALUES
    # --------------------------------------------------------

    order_units = int(
        inv["optimized_order_qty"]
        .sum()
    )

    order_value = float(
        inv["order_value"]
        .sum()
    )

    items_ordered = int(
        (
            inv["optimized_order_qty"]
            >
            0
        ).sum()
    )

    expected_shortage = float(
        inv["expected_shortage"]
        .sum()
    )

    high_risk = int(
        (
            inv["stockout_risk"]
            ==
            "HIGH"
        ).sum()
    )

    def card(title, value):

        return html.Div(
            [
                html.P(
                    title,
                    style={
                        "margin": "0",
                        "color": "#64748b"
                    }
                ),

                html.H2(
                    value
                )
            ],
            style=CARD_STYLE
        )

    cards = [

        card(
            "Order Units",
            f"{order_units:,}"
        ),

        card(
            "Order Value",
            f"${order_value:,.0f}"
        ),

        card(
            "Items Ordered",
            f"{items_ordered:,}"
        ),

        card(
            "Expected Shortage",
            f"{expected_shortage:,.0f}"
        ),

        card(
            "High-Risk Items",
            f"{high_risk:,}"
        )
    ]

    # --------------------------------------------------------
    # FORECAST
    # --------------------------------------------------------

    daily = (
        fc.groupby(
            "date",
            as_index=False
        )
        .agg(
            Actual=("sales", "sum"),
            Forecast=("pred_lightgbm", "sum"),
            Lower=("lgb_series_lower_90", "sum"),
            Upper=("lgb_series_upper_90", "sum")
        )
    )

    fig_forecast = go.Figure()

    fig_forecast.add_trace(
        go.Scatter(
            x=daily["date"],
            y=daily["Upper"],
            mode="lines",
            line={
                "width": 0
            },
            showlegend=False
        )
    )

    fig_forecast.add_trace(
        go.Scatter(
            x=daily["date"],
            y=daily["Lower"],
            mode="lines",
            fill="tonexty",
            name="90% Prediction Interval"
        )
    )

    fig_forecast.add_trace(
        go.Scatter(
            x=daily["date"],
            y=daily["Forecast"],
            mode="lines+markers",
            name="LightGBM Forecast"
        )
    )

    fig_forecast.add_trace(
        go.Scatter(
            x=daily["date"],
            y=daily["Actual"],
            mode="lines+markers",
            name="Actual Demand"
        )
    )

    fig_forecast.update_layout(
        title=
            f"Demand Forecast — {display_name}",
        xaxis_title="Date",
        yaxis_title="Units",
        hovermode="x unified",
        template="plotly_white"
    )

    # --------------------------------------------------------
    # MODEL PERFORMANCE
    # --------------------------------------------------------

    fig_model = px.bar(
        model_results,
        x="Model",
        y="WAPE_%",
        text="WAPE_%",
        title="Forecast Model Performance"
    )

    fig_model.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_model.update_layout(
        xaxis_title="",
        yaxis_title="WAPE (%)",
        template="plotly_white"
    )

    # --------------------------------------------------------
    # STOCKOUT RISK
    # --------------------------------------------------------

    risk = (
        inv["stockout_risk"]
        .value_counts()
        .rename_axis("Risk")
        .reset_index(name="Items")
    )

    fig_risk = px.pie(
        risk,
        names="Risk",
        values="Items",
        hole=0.45,
        title=
            f"Stockout Risk — {display_name}"
    )

    # --------------------------------------------------------
    # TOP ORDER ITEMS
    # --------------------------------------------------------

    top_orders = (
        inv[
            inv["optimized_order_qty"]
            >
            0
        ]
        .sort_values(
            "optimized_order_qty",
            ascending=False
        )
        .head(15)
        .sort_values(
            "optimized_order_qty"
        )
    )

    fig_order = px.bar(
        top_orders,
        x="optimized_order_qty",
        y="item_id",
        orientation="h",
        title=
            f"Top Replenishment Items — {display_name}"
    )

    fig_order.update_layout(
        xaxis_title="Recommended Units",
        yaxis_title="Item",
        template="plotly_white"
    )

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    table_cols = [
        "store_id",
        "item_id",
        "forecast_28d",
        "current_inventory",
        "safety_stock",
        "reorder_point",
        "optimized_order_qty",
        "expected_shortage",
        "inventory_cover_days",
        "stockout_risk",
        "order_value"
    ]

    table = (
        inv[table_cols]
        .sort_values(
            [
                "expected_shortage",
                "order_value"
            ],
            ascending=False
        )
        .copy()
    )

    numeric_cols = [
        "forecast_28d",
        "current_inventory",
        "safety_stock",
        "reorder_point",
        "expected_shortage",
        "inventory_cover_days",
        "order_value"
    ]

    for col in numeric_cols:

        table[col] = (
            table[col]
            .round(2)
        )

    dash_columns = [
        {
            "name":
                col.replace(
                    "_",
                    " "
                ).title(),

            "id":
                col
        }

        for col in table.columns
    ]

    return (
        cards,
        fig_forecast,
        fig_model,
        fig_risk,
        fig_order,
        table.to_dict("records"),
        dash_columns
    )


# ------------------------------------------------------------
# SERVER ENTRY POINT
# ------------------------------------------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            8050
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
