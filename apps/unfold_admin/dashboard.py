import json
from django.contrib.auth import get_user_model
from apps.checkout.models import Order

User = get_user_model()

def dashboard_callback(request, context):
    
    # Line Chart Data
    line_chart_data = {
        "labels": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        "datasets": [
            {
                "label": 'Received',
                "data": [10, 20, 15, 45, 30, 60, 50, 65, 80, 75, 60, 70],
                "borderColor": '#10916f', # <--- Your Custom Teal
                "backgroundColor": 'rgba(16, 145, 111, 0.2)', # Transparent Teal for the fill
                "fill": True,
                "tension": 0.4,
            },
            {
                "label": 'Due',
                "data": [5, 15, 25, 20, 35, 50, 45, 60, 75, 70, 55, 65],
                "borderColor": "#2dd4bf", # Due (Bright Mint/Teal)
                "backgroundColor": "rgba(45, 212, 191, 0.1)",# Transparent Orange for the fill
                "fill": True,
                "tension": 0.4,
            }
        ]
    }

    # Bar Chart Data
    bar_chart_data = {
        "labels": ['Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        "datasets": [
            {
                "label": 'Sales',
                "data": [40, 50, 45, 60, 20, 45, 60],
                "backgroundColor": '#10916f', # Your Custom Teal
                "borderRadius": 6,
            },
            {
                "label": 'Revenue',
                "data": [15, 25, 15, 10, 15, 25, 15],
                "backgroundColor": '#f97316', # Modern Orange
                "borderRadius": 6,
            }
        ]
    }

    # Context Update
    context.update({
        "total_views": "3.5K",
        "total_profit": "$4.2K",
        "total_products": "1.2K",
        "total_users": User.objects.count(),
        
        "line_chart_data": json.dumps(line_chart_data),
        "bar_chart_data": json.dumps(bar_chart_data),
        
        "recent_orders": Order.objects.select_related('user').order_by('-id')[:5],
    })

    return context