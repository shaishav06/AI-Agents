import EmailForm from "../components/EmailForm";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center">
      <h1 className="text-3xl font-bold mt-6">AI Business Assistant</h1>
      <div className="mt-6">
        <EmailForm />
      </div>
    </div>
  );
}
