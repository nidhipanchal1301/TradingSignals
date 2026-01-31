import { useEffect } from "react";
import { createCheckout } from "../api";

export default function Subscribe() {
  useEffect(() => {
    const checkout = async () => {
      try {
        const res = await createCheckout();
        window.location.href = res.data.url;
      } catch (err) {
        console.error(err);
      }
    };
    checkout();
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <p className="text-xl">Redirecting to payment...</p>
    </div>
  );
}
