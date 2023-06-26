export default function ({ $accessor, redirect }: any) {
  if (!$accessor.auth.isAuthenticated && !localStorage.getItem('access-token')) {
    return redirect('/');
  }
}
