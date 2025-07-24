@routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('is_admin'):
        return redirect('/login')
    
    user = User.query.get(session['user_id'])
    return render_template('user_dashboard.html', user=user)
