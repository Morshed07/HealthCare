from django.db import models
import json
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth
from django.contrib.auth import get_user_model
from apps.checkout.models import Order
from apps.product.models import Product
from apps.representative.models import Representative

User = get_user_model()


def get_percentage_change(current, previous):
    if previous > 0:
        return ((current - previous) / previous) * 100
    return 100 if current > 0 else 0


def dashboard_callback(request, context):
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # ==========================================
    # 1. CARD DATA & PERCENTAGES
    # ==========================================
    # Revenue (Current vs Previous Month)
    curr_rev = Order.objects.filter(paid=True, created_at__gte=start_of_month).aggregate(total=Sum('total'))['total'] or 0
    
    prev_month_end = start_of_month - timedelta(seconds=1)
    prev_month_start = prev_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    prev_rev = Order.objects.filter(paid=True, created_at__range=(prev_month_start, prev_month_end)).aggregate(total=Sum('total'))['total'] or 0
    
    rev_pct = get_percentage_change(curr_rev, prev_rev)

    # Overalls
    # total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_users = User.objects.filter(is_active=True, is_verified=True).count()
    total_representatives = Representative.objects.count()

    # ==========================================
    # 2. LINE CHART: Monthly Data (Current Year)
    # ==========================================
    line_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    paid_monthly = [0] * 12
    total_monthly = [0] * 12

    # Using ExtractMonth to safely get integers (1-12) across all database types
    monthly_stats = Order.objects.filter(created_at__year=now.year) \
        .annotate(month_num=ExtractMonth('created_at')) \
        .values('month_num') \
        .annotate(
            total_count=Count('id'), 
            paid_count=Count('id', filter=models.Q(paid=True))
        ) \
        .order_by('month_num')

    for stat in monthly_stats:
        m_idx = stat['month_num'] - 1  # 1 (Jan) becomes index 0
        paid_monthly[m_idx] = stat['paid_count']
        total_monthly[m_idx] = stat['total_count']

    line_chart_data = {
        "labels": line_labels,
        "datasets": [
            {
                "label": 'Paid Orders',
                "data": paid_monthly,
                "borderColor": "#12ac83",
                "backgroundColor": 'rgba(18, 172, 131, 0.2)',
                "fill": True, "tension": 0.4,
            },
            {
                "label": 'Total Orders',
                "data": total_monthly,
                "borderColor": "#9a41e2",
                "backgroundColor": "rgba(154, 65, 226, 0.1)",
                "fill": True, "tension": 0.4,
            }
        ]
    }

    # ==========================================
    # 3. BAR CHART: Daily Orders (Last 7 Days)
    # ==========================================
    last_7_days = [(now - timedelta(days=i)).date() for i in range(6, -1, -1)]
    bar_labels = [d.strftime('%a') for d in last_7_days]
    daily_counts = [0] * 7

    # Group by the native __date lookup for safety
    daily_stats = Order.objects.filter(created_at__date__in=last_7_days) \
        .values('created_at__date') \
        .annotate(count=Count('id'))

    stats_dict = {stat['created_at__date']: stat['count'] for stat in daily_stats}
    
    for i, date in enumerate(last_7_days):
        daily_counts[i] = stats_dict.get(date, 0)

    bar_chart_data = {
        "labels": bar_labels,
        "datasets": [{
            "label": 'Daily Orders',
            "data": daily_counts,
            "backgroundColor": '#12ac83',
            "borderRadius": 6,
        }]
    }

    # ==========================================
    # 4. CONTEXT UPDATE
    # ==========================================
    context.update({
        "total_revenue": f"${curr_rev:,.1f}",
        "revenue_pct": f"{abs(rev_pct):.1f}% {'↑' if rev_pct >= 0 else '↓'}",
        "revenue_color": "text-green-500" if rev_pct >= 0 else "text-red-500",
        
        "total_representatives": total_representatives,
        "total_products": total_products,
        "total_users": total_users,
        
        "line_chart_data": json.dumps(line_chart_data),
        "bar_chart_data": json.dumps(bar_chart_data),
        "recent_orders": Order.objects.select_related('user').order_by('-id')[:10],
    })

    return context