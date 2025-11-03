import Dashboard from './views/dashboard'
import Login from './views/login';
import { useState } from 'react';


function App() {
	const [token, setToken] = useState<string | null>(null);

	return token ? (
		<Dashboard token={token} />
	) : (
		<Login onLogin={setToken} />
	);
}

export default App;
