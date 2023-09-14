from django.urls import path
from travel_app import views

urlpatterns = [
    path('postlist/',views.postList),
    path('postcreate/',views.postCreate),
    path('postdetail/<int:plan_id>/',views.postDetail),
    path('postdelete/<int:plan_id>/',views.postDelete),
    path('regiondetail/<int:region_id>/',views.regionDetail),
    path('booking/<int:plan_id>/',views.bookingForm),
    path('booking_success/<int:plan_id>/<int:booking_id>/',views.bookingSuccess),
    path('users/<int:user_id>/',views.usersTable),
    path('bookings/<int:user_id>/',views.bookingsTable),
    path('booking_status_confirm/<int:user_id>/<int:booking_id>/',views.bookingStatusConfirm),
    path('plans/<int:user_id>/',views.plansTable),
    path('mybookings/<int:user_id>/<int:currentuser_id>/',views.userBookings),
    path('booking_cancel/<int:user_id>/<int:currentuser_id>/<int:booking_id>/',views.bookingCancel),
    path('review_create/<int:user_id>/<int:plan_id>/',views.reviewCreate),
    path('review_delete/<int:review_id>/<int:plan_id>/',views.reviewDelete),
    path('review_edit/<int:review_id>/<int:plan_id>/',views.reviewEdit),
    path('search_by/',views.searchBy),
]
