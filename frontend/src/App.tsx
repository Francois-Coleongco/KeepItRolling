import Dashboard from './views/dashboard'
import Login from './views/login';
import { BrowserRouter, Route, Routes } from 'react-router-dom';


function App() {
	return (
		<Routes>
			<Route
				path="/login"
				element={<Login />}
			/>
			<Route
				path="/dashboard"
				element={<Dashboard />}
			/>
		</Routes>
	);

}

export default App;
