import { useState, type FormEvent, type ChangeEvent } from "react";

interface LoginProps {
	onLogin: (token: string) => void;
}

const Login = ({ onLogin }: LoginProps) => {
	const [username, setUsername] = useState<string>("");
	const [password, setPassword] = useState<string>("");
	const [loading, setLoading] = useState<boolean>(false);
	const [error, setError] = useState<string>("");

	const handleLogin = async (e: FormEvent) => {
		e.preventDefault();
		setLoading(true);

		try {
			const formData = new URLSearchParams();
			formData.append("username", username);
			formData.append("password", password);

			const res = await fetch("http://127.0.0.1:8000/token", {
				method: "POST",
				headers: { "Content-Type": "application/x-www-form-urlencoded" },
				body: formData.toString(),
			});

			if (!res.ok) {
				throw new Error("Invalid username or password");
			}

			const data = await res.json();
			onLogin(data.access_token);
		} catch (err: any) {
			setError(err.message || "Login failed");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="min-h-screen flex items-center justify-center bg-gray-900 text-gray-200 font-sans p-4">
			<form
				onSubmit={handleLogin}
				className="bg-gray-800 p-8 rounded shadow-md w-full max-w-sm flex flex-col gap-4"
			>
				<h1 className="text-3xl font-bold text-indigo-400 mb-4 text-center">
					Login
				</h1>

				{error && (
					<div className="bg-red-600 text-white p-2 rounded text-sm">{error}</div>
				)}

				<input
					type="text"
					placeholder="Username"
					value={username}
					onChange={(e: ChangeEvent<HTMLInputElement>) =>
						setUsername(e.target.value)
					}
					className="bg-gray-700 text-gray-200 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
					required
				/>
				<input
					type="password"
					placeholder="Password"
					value={password}
					onChange={(e: ChangeEvent<HTMLInputElement>) =>
						setPassword(e.target.value)
					}
					className="bg-gray-700 text-gray-200 px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
					required
				/>

				<button
					type="submit"
					className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition"
					disabled={loading}
				>
					{loading ? "Logging in..." : "Login"}
				</button>
			</form>
		</div>
	);
};

export default Login
