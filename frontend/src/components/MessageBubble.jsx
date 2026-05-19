export default function MessageBubble({ role, text }) {
  const className = role === "user" ? "bubble user" : "bubble assistant";
  return (
    <div className={className}>
      <p>{text}</p>
    </div>
  );
}
