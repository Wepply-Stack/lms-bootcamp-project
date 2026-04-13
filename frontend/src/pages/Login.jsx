
import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [focused, setFocused] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => setLoading(false), 2000);
  };

  return (
    <div className="min-h-screen bg-green-950 flex items-center justify-center p-4 relative overflow-hidden">


      {/* Glow orb */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-amber-700 opacity-10 rounded-full blur-3xl pointer-events-none" />

      {/* Card */}
      <div className="relative w-full max-w-2xl">

        {/* Top accent bar */}
        <div className="h-px bg-gradient-to-r from-transparent via-amber-500 to-transparent mb-8" />

        <div className="bg-yellow-50 border border-green-800 rounded-2xl p-10 shadow-2xl shadow-black/60">

          {/* Logo / brand mark */}
          <div className="flex items-center gap-3 mb-10">
            <div className="w-8 h-8 bg-amber-500 rounded rotate-45 flex items-center justify-center">
              <div className="w-3 h-3 bg-green-950 rounded-sm rotate-45" />
            </div>
            <span
              className="text-green-900 text-xl tracking-widest uppercase"
              style={{ fontFamily: "'Georgia', serif", letterSpacing: "0.25em" }}
            >
              LOGO HERE
            </span>
          </div>

          {/* Heading */}
          <h1
            className="text-5xl text-green-900 mb-1"
            style={{ fontFamily: "'Georgia', serif", fontWeight: 400 }}
          >
            Welcome
          </h1>
          <p className="text-green-900 text-md tracking-wide mb-8">
            Sign in to continue to your account.
          </p>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-5">

            {/* Email */}
            <div>
              <label className="block text-md uppercase tracking-widest text-green-700 mb-2">
                Email address
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onFocus={() => setFocused("email")}
                onBlur={() => setFocused(null)}
                placeholder="you@example.com"
                className={`w-full bg-stone-200 border rounded-lg px-4 py-3 text-green-900 placeholder-green-600 text-md outline-none transition-all duration-200 ${
                  focused === "email"
                    ? "border-amber-500 ring-1 ring-amber-500/30"
                    : "border-green-700 hover:border-green-600"
                }`}
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-md uppercase tracking-widest text-green-700 mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onFocus={() => setFocused("password")}
                  onBlur={() => setFocused(null)}
                  placeholder="••••••••"
                  className={`w-full bg-stone-200 border rounded-lg px-4 py-3 pr-12 text-green-900 placeholder-green-600 text-sm outline-none transition-all duration-200 ${
                    focused === "password"
                      ? "border-amber-500 ring-1 ring-amber-500/30"
                      : "border-green-700 hover:border-green-600"
                  }`}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-green-600 hover:text-green-300 transition-colors"
                >
                  {showPassword ? (
                    <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18" />
                    </svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {/* Remember / Forgot */}
            <div className="flex items-center justify-between pt-1">
              <label className="flex items-center gap-2 cursor-pointer group">
                <div className="relative">
                  <input type="checkbox" className="sr-only peer" />
                  <div className="w-4 h-4 border border-green-600 rounded bg-green-800 peer-checked:bg-amber-500 peer-checked:border-amber-500 transition-all" />
                  <svg
                    className="absolute top-0.5 left-0.5 w-3 h-3 text-green-950 opacity-0 peer-checked:opacity-100 transition-opacity"
                    viewBox="0 0 12 12"
                    fill="none"
                  >
                    <path d="M2 6l3 3 5-5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
                <span className="text-xs text-green-500 group-hover:text-green-400 transition-colors">
                  Remember me
                </span>
              </label>
              <a href="#" className="text-xs text-amber-500/80 hover:text-amber-400 transition-colors tracking-wide">
                Forgot password?
              </a>
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full mt-2 relative overflow-hidden bg-amber-500 hover:bg-amber-400 disabled:bg-amber-800 text-green-950 font-semibold text-sm tracking-widest uppercase py-3.5 rounded-lg transition-all duration-200 group"
            >
              <span className={`transition-all duration-200 ${loading ? "opacity-0" : "opacity-100"}`}>
                Sign In
              </span>
              {loading && (
                <span className="absolute inset-0 flex items-center justify-center">
                  <svg className="animate-spin w-5 h-5 text-green-950" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                  </svg>
                </span>
              )}
            </button>

          </form>

        

        
        </div>

      </div>
    </div>
  );
}