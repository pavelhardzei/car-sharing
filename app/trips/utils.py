from django.utils import timezone


def get_total_cost(trip):
    total_cost = 0
    total_cost += trip.total_cost
    if trip.reservation_time:
        total_cost += trip.reservation_time * trip.state.reservation_price
    current_time = timezone.now()
    total_cost += (current_time - trip.start_date).total_seconds() / 3600 * trip.state.fare

    return total_cost, current_time
