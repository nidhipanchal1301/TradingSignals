import { useEffect, useState } from "react";
import { getSignals } from "../api/signals.api";
import { createCheckout, getBillingStatus } from "../api/billing.api";
import SignalCard from "../components/SignalCard";
import Navbar from "../components/Navbar";

export default function Dashboard() {
  const [signals, setSignals] = useState([]);
  const [paid, setPaid] = useState(false);
  const [loading, setLoading] = useState(true);

  // 1️⃣ Check subscription status on load
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await getBillingStatus();
        setPaid(res.data.is_paid);
      } catch (err) {
        console.error("Billing status error", err);
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
  }, []);

  // 2️⃣ Fetch signals when paid/free changes
  useEffect(() => {
    if (!loading) {
      getSignals(paid)
        .then(res => setSignals(res.data))
        .catch(err => console.error("Signals error", err));
    }
  }, [paid, loading]);

  // 3️⃣ Redirect to Stripe checkout
  const subscribe = async () => {
    try {
      const res = await createCheckout();
      window.location.href = res.data.checkout_url;
    } catch (err) {
      console.error("Checkout error", err);
    }
  };

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="dashboard">Loading...</div>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="dashboard">
        {!paid && (
          <button className="subscribe-btn" onClick={subscribe}>
            Subscribe ₹499
          </button>
        )}

        <div className="signals-grid">
          {signals.map((s, i) => (
            <SignalCard key={i} signal={s} />
          ))}
        </div>
      </div>
    </>
  );
}
