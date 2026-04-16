import { initializeApp } from "firebase/app";
import { getAnalytics, isSupported } from "firebase/analytics";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const rawConfig = import.meta.env.VITE_FIREBASE_CONFIG;

if (!rawConfig) {
  throw new Error("Missing VITE_FIREBASE_CONFIG");
}

const firebaseConfig = JSON.parse(rawConfig);
const app = initializeApp(firebaseConfig);

isSupported().then((supported) => {
  if (supported) {
    getAnalytics(app);
  }
});

export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
