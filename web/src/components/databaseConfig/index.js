import { initializeApp } from "firebase/app";
import { getFirestore } from "@firebase/firestore";

function InitFirebase() {
  const firebaseConfig = {
    apiKey: process.env.firebaseApiKey,
    authDomain: process.env.firebaseAuthDomain,
    databaseURL: process.env.firebaseDatabaseURL,
    projectId: process.env.firebaseProjectId,
    storageBucket: process.env.firebaseStorageBucket,
    messagingSenderId: process.env.firebaseMessagingSenderId,
    appId: process.env.firebaseAppId,
  };
  const app = initializeApp(firebaseConfig);
  return getFirestore(app);
}

export default InitFirebase;
