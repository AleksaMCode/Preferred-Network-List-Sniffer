import { initializeApp } from "firebase/app";
import { getFirestore } from "@firebase/firestore";

function InitFirebase() {
  const firebaseConfig = {
    apiKey: process.env.REACT_APP_apiKey,
    authDomain: process.env.REACT_APP_authDomain,
    databaseURL: process.env.REACT_APP_databaseURL,
    projectId: process.env.REACT_APP_projectId,
    storageBucket: process.env.REACT_APP_storageBucket,
    messagingSenderId: process.env.REACT_APP_messagingSenderId,
    appId: process.env.REACT_APP_appId,
  };
  const app = initializeApp(firebaseConfig);
  return getFirestore(app);
}

export default InitFirebase;
