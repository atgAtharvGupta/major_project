import { useMemo, useState } from "react";
import { signInWithPopup, signOut } from "firebase/auth";

import { auth, googleProvider } from "./firebase";

const streamlitHint = "Paste the Firebase ID token into the Streamlit sidebar Google Token form.";

export default function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState("");
  const [error, setError] = useState("");

  const streamlitUrl = useMemo(() => import.meta.env.VITE_STREAMLIT_URL || "http://localhost:8501", []);

  async function handleSignIn() {
    setError("");
    try {
      const result = await signInWithPopup(auth, googleProvider);
      const idToken = await result.user.getIdToken();
      setUser(result.user);
      setToken(idToken);
    } catch (signInError) {
      setError(signInError.message || "Google sign-in failed");
    }
  }

  async function handleSignOut() {
    await signOut(auth);
    setUser(null);
    setToken("");
  }

  return (
    <main style={styles.page}>
      <section style={styles.card}>
        <h1 style={styles.title}>Finance Assistant Auth</h1>
        <p style={styles.subtle}>Use Google sign-in here, then hand the Firebase ID token to the Streamlit app.</p>
        {!user ? (
          <button style={styles.button} onClick={handleSignIn}>
            Sign in with Google
          </button>
        ) : (
          <>
            <div style={styles.infoRow}>
              <span>Signed in as</span>
              <strong>{user.email}</strong>
            </div>
            <textarea readOnly value={token} style={styles.textarea} />
            <p style={styles.subtle}>{streamlitHint}</p>
            <div style={styles.actions}>
              <a href={streamlitUrl} style={styles.link} target="_blank" rel="noreferrer">
                Open Streamlit
              </a>
              <button style={styles.buttonSecondary} onClick={handleSignOut}>
                Sign out
              </button>
            </div>
          </>
        )}
        {error ? <p style={styles.error}>{error}</p> : null}
      </section>
    </main>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#0f0f10",
    color: "#f5f5f5",
    display: "grid",
    placeItems: "center",
    fontFamily: "Inter, Arial, sans-serif",
  },
  card: {
    width: "min(720px, 92vw)",
    background: "#171718",
    border: "1px solid #2e2e31",
    borderRadius: "18px",
    padding: "32px",
    boxShadow: "0 12px 40px rgba(0, 0, 0, 0.28)",
  },
  title: {
    marginTop: 0,
    marginBottom: "0.5rem",
  },
  subtle: {
    color: "#c8c8cc",
    lineHeight: 1.5,
  },
  infoRow: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: "1rem",
    marginBottom: "1rem",
  },
  textarea: {
    width: "100%",
    minHeight: "220px",
    background: "#0f0f10",
    color: "#f5f5f5",
    border: "1px solid #323236",
    borderRadius: "12px",
    padding: "12px",
  },
  actions: {
    display: "flex",
    gap: "12px",
    marginTop: "1rem",
    alignItems: "center",
  },
  button: {
    background: "#f5f5f5",
    color: "#111",
    border: 0,
    borderRadius: "999px",
    padding: "12px 18px",
    cursor: "pointer",
  },
  buttonSecondary: {
    background: "#1d1d20",
    color: "#f5f5f5",
    border: "1px solid #3a3a3f",
    borderRadius: "999px",
    padding: "12px 18px",
    cursor: "pointer",
  },
  link: {
    color: "#f5f5f5",
  },
  error: {
    color: "#ff9f9f",
    marginTop: "1rem",
  },
};
