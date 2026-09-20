from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import TourPackage, Booking, Payment


def home(request):
    return render(request, 'travel/home.html')


@login_required
def dashboard(request):

    bookings = Booking.objects.filter(
        user=request.user
    )

    total_bookings = bookings.count()

    pending_bookings = bookings.filter(
        status='Pending'
    ).count()

    confirmed_bookings = bookings.filter(
        status='Confirmed'
    ).count()

    total_payments = Payment.objects.filter(
        booking__user=request.user
    ).count()

    available_seats = sum(
        package.available_seats
        for package in TourPackage.objects.all()
    )

    return render(
        request,
        'travel/dashboard.html',
        {
            'bookings': bookings,
            'total_bookings': total_bookings,
            'pending_bookings': pending_bookings,
            'confirmed_bookings': confirmed_bookings,
            'total_payments': total_payments,
            'available_seats': available_seats,
        }
    )


def packages(request):

    search_query = request.GET.get(
        'search',
        ''
    )

    if search_query:

        tour_packages = TourPackage.objects.filter(
            package_name__icontains=search_query
        )

    else:

        tour_packages = TourPackage.objects.all()

    return render(
        request,
        'travel/packages.html',
        {
            'tour_packages': tour_packages
        }
    )


@login_required
def booking(request, package_id):

    package = get_object_or_404(
        TourPackage,
        id=package_id
    )

    if request.method == 'POST':

        customer_name = request.POST.get(
            'customer_name'
        )

        customer_email = request.POST.get(
            'customer_email'
        )

        number_of_people = int(
            request.POST.get(
                'number_of_people',
                1
            )
        )

        transportation_upgrade = request.POST.get(
            'transportation_upgrade',
            'No'
        )

        if number_of_people <= 0:

            messages.error(
                request,
                'Number of people must be at least 1.'
            )

            return redirect(
                'booking',
                package_id=package.id
            )

        if number_of_people > package.available_seats:

            messages.error(
                request,
                'Not enough seats available.'
            )

            return redirect(
                'booking',
                package_id=package.id
            )

        transportation_price = 0

        if transportation_upgrade == 'Standard':

            transportation_price = 1000

        elif transportation_upgrade == 'Premium':

            transportation_price = 2500

        total_transportation_price = (
            transportation_price
            * number_of_people
        )

        booking = Booking.objects.create(

            user=request.user,

            customer_name=customer_name,

            customer_email=customer_email,

            tour_package=package,

            number_of_people=number_of_people,

            transportation_upgrade=transportation_upgrade,

            transportation_price=total_transportation_price,

            status='Pending'
        )

        package.available_seats -= number_of_people

        package.save()

        messages.success(
            request,
            'Your booking has been created successfully.'
        )

        return redirect(
            'my_bookings'
        )

    return render(
        request,
        'travel/booking.html',
        {
            'package': package
        }
    )


def register(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        email = request.POST.get(
            'email'
        )

        password = request.POST.get(
            'password'
        )

        confirm_password = request.POST.get(
            'confirm_password'
        )

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect(
                'register'
            )

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect(
                'register'
            )

        User.objects.create_user(

            username=username,

            email=email,

            password=password
        )

        messages.success(
            request,
            'Registration successful. Please login.'
        )

        return redirect(
            'login'
        )

    return render(
        request,
        'travel/register.html'
    )


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect(
                'dashboard'
            )

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(
        request,
        'travel/login.html'
    )


def admin_login(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:

            login(
                request,
                user
            )

            return redirect(
                'admin_dashboard'
            )

        else:

            messages.error(
                request,
                'Invalid admin username or password.'
            )

    return render(
        request,
        'travel/admin_login.html'
    )


def admin_dashboard(request):

    if not request.user.is_authenticated:

        return redirect(
            'admin_login'
        )

    if not request.user.is_staff:

        messages.error(
            request,
            'You are not authorized to access the admin dashboard.'
        )

        return redirect(
            'dashboard'
        )

    total_users = User.objects.count()

    total_packages = TourPackage.objects.count()

    total_bookings = Booking.objects.count()

    total_payments = Payment.objects.count()

    available_seats = sum(
        package.available_seats
        for package in TourPackage.objects.all()
    )

    recent_bookings = Booking.objects.select_related(
        'tour_package',
        'user'
    ).order_by(
        '-booking_date'
    )[:5]

    return render(
        request,
        'travel/admin_dashboard.html',
        {
            'total_users': total_users,
            'total_packages': total_packages,
            'total_bookings': total_bookings,
            'total_payments': total_payments,
            'available_seats': available_seats,
            'recent_bookings': recent_bookings,
        }
    )


@login_required
def user_logout(request):

    logout(request)

    return redirect(
        'login'
    )


@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).select_related(
        'tour_package'
    ).order_by(
        '-booking_date'
    )

    return render(
        request,
        'travel/my_bookings.html',
        {
            'bookings': bookings
        }
    )


@login_required
def payment(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if request.method == 'POST':

        payment_method = request.POST.get(
            'payment_method'
        )

        Payment.objects.create(

            booking=booking,

            amount=(
                booking.tour_package.price
                * booking.number_of_people
            )
            + booking.transportation_price,

            payment_method=payment_method,

            status='Paid'
        )

        booking.status = 'Confirmed'

        booking.save()

        messages.success(
            request,
            'Payment completed successfully.'
        )

        return redirect(
            'my_bookings'
        )

    total_amount = (
        booking.tour_package.price
        * booking.number_of_people
    ) + booking.transportation_price

    return render(
        request,
        'travel/payment.html',
        {
            'booking': booking,
            'total_amount': total_amount
        }
    )