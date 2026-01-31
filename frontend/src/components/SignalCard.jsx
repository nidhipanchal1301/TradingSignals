export default function SignalCard({ signal }) {
  return (
    <div className="signal-card">
      <h3>{signal.symbol}</h3>
      <p>{signal.action}</p>
      <span>₹ {signal.price}</span>
    </div>
  );
}
