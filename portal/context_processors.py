def base_template(request):
    """
    Globally provides the correct base template path for INGRES-AI.
    base_public.html: For Landing, About, Contact (Navbar)[cite: 579, 844].
    base_dashboard.html: For Public/Official Dashboard (Sidebar)[cite: 580].
    """
    if request.user.is_authenticated:
        return {"base_template": "base_dashboard.html"}
    return {"base_template": "base_public.html"}