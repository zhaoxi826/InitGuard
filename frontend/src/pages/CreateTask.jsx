import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import api from '../api';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import Input from '../components/Input';

const CreateTask = () => {
  const navigate = useNavigate();
  const [taskName, setTaskName] = useState('');
  const [databaseId, setDatabaseId] = useState('');
  const [ossId, setOssId] = useState('');
  const [databaseName, setDatabaseName] = useState('');
  const [error, setError] = useState('');

  const [databases, setDatabases] = useState([]);
  const [ossList, setOssList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResources = async () => {
      try {
        const response = await api.get('/resource/list');
        setDatabases(response.data.databases);
        setOssList(response.data.oss);
        // Set defaults if available
        if (response.data.databases.length > 0) setDatabaseId(response.data.databases[0].resource_id);
        if (response.data.oss.length > 0) setOssId(response.data.oss[0].resource_id);
      } catch (err) {
        console.error("Failed to fetch resources", err);
        setError("Failed to load resources. Please create resources first.");
      } finally {
        setLoading(false);
      }
    };
    fetchResources();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!databaseId || !ossId) {
        setError("Please select a database and OSS storage.");
        return;
    }

    try {
      await api.post('/task/create', {
        task_name: taskName,
        database_id: parseInt(databaseId),
        oss_id: parseInt(ossId),
        database_name: databaseName,
        task_type: 'backup_task'
      });
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create task');
    }
  };

  if (loading) return <Layout><div>Loading...</div></Layout>;

  return (
    <Layout>
      <div className="max-w-2xl mx-auto bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Create New Task</h2>

        {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Task Name</label>
            <Input value={taskName} onChange={(e) => setTaskName(e.target.value)} required />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Target Database (Resource)</label>
            <select
              value={databaseId}
              onChange={(e) => setDatabaseId(e.target.value)}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              required
            >
              <option value="">Select Database Resource</option>
              {databases.map(db => (
                <option key={db.resource_id} value={db.resource_id}>{db.resource_name} ({db.host})</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Database Name (Schema/DB)</label>
            <Input value={databaseName} onChange={(e) => setDatabaseName(e.target.value)} required placeholder="e.g. postgres" />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Target OSS (Storage)</label>
            <select
              value={ossId}
              onChange={(e) => setOssId(e.target.value)}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              required
            >
               <option value="">Select OSS Resource</option>
              {ossList.map(oss => (
                <option key={oss.resource_id} value={oss.resource_id}>{oss.resource_name} ({oss.endpoint})</option>
              ))}
            </select>
          </div>

          <div className="pt-4">
            <Button type="submit">Create Task</Button>
          </div>
        </form>
      </div>
    </Layout>
  );
};

export default CreateTask;
