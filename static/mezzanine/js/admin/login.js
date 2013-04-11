$(function() {
    // Fix the ``Home`` breadcrumb link non logged-in views.
    var home = $('.breadcrumbs a:first');
    if (home.length == 1) {
        home.attr('href', window.__admin_url);
    }
    document.getElementById('username_input').focus();
});
