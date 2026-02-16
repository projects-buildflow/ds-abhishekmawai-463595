from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_data(base_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load orders, products, and order_items data."""
    orders = pd.read_csv(
        base_dir / "data" / "orders.csv",
        parse_dates=["order_date"],
    )
    products = pd.read_csv(base_dir / "data" / "products.csv")
    order_items = pd.read_csv(base_dir / "data" / "order_items.csv")
    return orders, products, order_items


def compute_kpis(
    orders: pd.DataFrame, products: pd.DataFrame, order_items: pd.DataFrame
) -> dict:
    """
    Compute business KPIs for the executive dashboard.

    Assumptions:
    - Revenue and active customers are based only on orders with status == "delivered".
    - Top products by revenue are calculated from delivered order items.
    """
    delivered_orders = orders[orders["status"] == "delivered"].copy()

    # Total revenue from delivered orders
    total_revenue = float(delivered_orders["total"].sum()) if not delivered_orders.empty else 0.0

    # Active customers (monthly): total number of distinct customers with delivered orders
    if not delivered_orders.empty:
        active_customers = int(delivered_orders["customer_id"].nunique())
    else:
        active_customers = 0

    # Average order value (AOV) on delivered orders
    if not delivered_orders.empty:
        avg_order_value = total_revenue / len(delivered_orders)
    else:
        avg_order_value = 0.0

    # Top 5 products by revenue (from delivered orders only)
    delivered_order_ids = set(delivered_orders["order_id"].unique())
    delivered_items = order_items[order_items["order_id"].isin(delivered_order_ids)].copy()

    # Ensure numeric
    delivered_items["item_total"] = pd.to_numeric(
        delivered_items["item_total"], errors="coerce"
    ).fillna(0)

    product_revenue = (
        delivered_items.groupby("product_id", as_index=False)["item_total"].sum()
    )
    product_revenue = product_revenue.rename(columns={"item_total": "revenue"})

    product_revenue = product_revenue.merge(
        products[["id", "name"]],
        left_on="product_id",
        right_on="id",
        how="left",
    )

    product_revenue = product_revenue.sort_values("revenue", ascending=False)
    top5 = product_revenue.head(5).copy()

    top_product_names = top5["name"].fillna(top5["product_id"]).tolist()
    # Pad to exactly 5 entries if needed
    while len(top_product_names) < 5:
        top_product_names.append("")

    return {
        "total_revenue": total_revenue,
        "active_customers": active_customers,
        "avg_order_value": avg_order_value,
        "top_products": top_product_names,
        "delivered_orders": delivered_orders,
        "product_revenue_top5": top5,
    }


def export_metrics_csv(kpis: dict, output_path: Path) -> None:
    """Export KPIs in the exact metrics.csv format required."""
    rows: list[dict[str, str]] = []

    rows.append(
        {
            "metric": "total_revenue",
            "value": f"{kpis['total_revenue']:.2f}",
        }
    )
    rows.append(
        {
            "metric": "active_customers",
            "value": str(kpis["active_customers"]),
        }
    )
    rows.append(
        {
            "metric": "avg_order_value",
            "value": f"{kpis['avg_order_value']:.2f}",
        }
    )

    for idx, name in enumerate(kpis["top_products"], start=1):
        rows.append(
            {
                "metric": f"top_product_{idx}",
                "value": str(name),
            }
        )

    df = pd.DataFrame(rows, columns=["metric", "value"])
    df.to_csv(output_path, index=False)


def create_dashboard_figure(kpis: dict, output_path: Path) -> None:
    """Create a static dashboard image with KPI cards and charts."""
    sns.set_theme(style="whitegrid")

    delivered_orders: pd.DataFrame = kpis["delivered_orders"]
    top5: pd.DataFrame = kpis["product_revenue_top5"]

    fig = plt.figure(figsize=(14, 8))
    fig.suptitle("Executive Revenue Dashboard", fontsize=18, fontweight="bold")

    # Layout: 2 rows, 3 KPI cards in row 1, 2 charts in row 2
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 2])

    # KPI 1: Total Revenue
    ax_kpi1 = fig.add_subplot(gs[0, 0])
    ax_kpi1.axis("off")
    ax_kpi1.set_title("Total Revenue (Delivered)", fontsize=12, fontweight="bold")
    ax_kpi1.text(
        0.5,
        0.4,
        f"₹{kpis['total_revenue']:,.0f}",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="#1f77b4",
    )

    # KPI 2: Active Customers (Latest Month)
    ax_kpi2 = fig.add_subplot(gs[0, 1])
    ax_kpi2.axis("off")
    ax_kpi2.set_title("Active Customers (Latest Month)", fontsize=12, fontweight="bold")
    ax_kpi2.text(
        0.5,
        0.4,
        f"{kpis['active_customers']:,}",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="#2ca02c",
    )

    # KPI 3: Average Order Value
    ax_kpi3 = fig.add_subplot(gs[0, 2])
    ax_kpi3.axis("off")
    ax_kpi3.set_title("Average Order Value", fontsize=12, fontweight="bold")
    ax_kpi3.text(
        0.5,
        0.4,
        f"₹{kpis['avg_order_value']:,.0f}",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="#d62728",
    )

    # Chart 1: Monthly Revenue Trend (Line chart)
    ax_line = fig.add_subplot(gs[1, :2])
    if not delivered_orders.empty:
        monthly = (
            delivered_orders.assign(month=delivered_orders["order_date"].dt.to_period("M"))
            .groupby("month")["total"]
            .sum()
            .reset_index()
        )
        monthly["month_str"] = monthly["month"].astype(str)
        sns.lineplot(
            data=monthly,
            x="month_str",
            y="total",
            marker="o",
            ax=ax_line,
            color="#1f77b4",
        )
        ax_line.set_title("Monthly Revenue Trend (Delivered Orders)", fontsize=12, fontweight="bold")
        ax_line.set_xlabel("Month")
        ax_line.set_ylabel("Revenue (₹)")
        ax_line.tick_params(axis="x", rotation=45)
    else:
        ax_line.text(
            0.5,
            0.5,
            "No delivered orders available for trend.",
            ha="center",
            va="center",
        )
        ax_line.axis("off")

    # Chart 2: Top 5 Products by Revenue (Bar chart)
    ax_bar = fig.add_subplot(gs[1, 2])
    if not top5.empty:
        top5_plot = top5.copy()
        top5_plot["label"] = top5_plot["name"].fillna(top5_plot["product_id"])
        top5_plot = top5_plot.sort_values("revenue", ascending=True)
        sns.barplot(
            data=top5_plot,
            x="revenue",
            y="label",
            ax=ax_bar,
            palette="Blues_r",
        )
        ax_bar.set_title("Top 5 Products by Revenue", fontsize=12, fontweight="bold")
        ax_bar.set_xlabel("Revenue (₹)")
        ax_bar.set_ylabel("")
    else:
        ax_bar.text(
            0.5,
            0.5,
            "No product revenue data.",
            ha="center",
            va="center",
        )
        ax_bar.axis("off")

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> None:
    # project_root: .../ds-abhishekmawai-463595
    project_root = Path(__file__).resolve().parents[2]
    dashboard_dir = Path(__file__).resolve().parent
    dashboard_dir.mkdir(parents=True, exist_ok=True)

    orders, products, order_items = load_data(project_root)
    kpis = compute_kpis(orders, products, order_items)

    # Export metrics.csv into submissions/dashboard/
    metrics_path = dashboard_dir / "metrics.csv"
    export_metrics_csv(kpis, metrics_path)

    # Create dashboard.png into submissions/dashboard/
    dashboard_path = dashboard_dir / "dashboard.png"
    create_dashboard_figure(kpis, dashboard_path)


if __name__ == "__main__":
    main()

