import React, { useState } from 'react';
import Layout from '../components/Layout';
import api from '../api';
import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';
import Input from '../components/Input';

const CreateResource = () => {
  const navigate = useNavigate();
  const [resourceType, setResourceType] = useState('database');
  const [resourceName, setResourceName] = useState('');
  const [error, setError] = useState('');

  // Database fields
  const [dbType, setDbType] = useState('postgres');
  const [host, setHost] = useState('');
  const [port, setPort] = useState('5432');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // OSS fields
  const [ossType, setOssType] = useState('minio');
  const [endpoint, setEndpoint] = useState('');
  const [accessKey, setAccessKey] = useState('');
  const [secretKey, setSecretKey] = useState('');
  const [bucket, setBucket] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    let resourceValue;
    if (resourceType === 'database') {
      resourceValue = {
        type: 'database',
        database_type: dbType,
        host,
        port: parseInt(port),
        username,
        password
      };
    } else {
      resourceValue = {
        type: 'oss',
        oss_type: ossType,
        endpoint,
        access_key: accessKey,
        secret_key: secretKey,
        bucket
      };
    }

    try {
      await api.post('/resource/create', {
        resource_name: resourceName,
        resource_value: resourceValue
      });
      navigate('/');
    } catch (err) {
        console.error(err);
      setError(err.response?.data?.detail || 'Failed to create resource');
    }
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white">Create New Resource</h2>

        {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Resource Name</label>
            <Input value={resourceName} onChange={(e) => setResourceName(e.target.value)} required />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Resource Type</label>
            <select
              value={resourceType}
              onChange={(e) => setResourceType(e.target.value)}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            >
              <option value="database">Database</option>
              <option value="oss">Object Storage (OSS)</option>
            </select>
          </div>

          {resourceType === 'database' && (
            <div className="space-y-4 border-t pt-4 dark:border-gray-700">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Database Type</label>
                <select
                  value={dbType}
                  onChange={(e) => setDbType(e.target.value)}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                >
                  <option value="postgres">PostgreSQL</option>
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Host</label>
                  <Input value={host} onChange={(e) => setHost(e.target.value)} required />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Port</label>
                  <Input type="number" value={port} onChange={(e) => setPort(e.target.value)} required />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Username</label>
                <Input value={username} onChange={(e) => setUsername(e.target.value)} required />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Password</label>
                <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
              </div>
            </div>
          )}

          {resourceType === 'oss' && (
            <div className="space-y-4 border-t pt-4 dark:border-gray-700">
               <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">OSS Type</label>
                <select
                  value={ossType}
                  onChange={(e) => setOssType(e.target.value)}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                >
                  <option value="minio">MinIO</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Endpoint</label>
                <Input value={endpoint} onChange={(e) => setEndpoint(e.target.value)} required placeholder="http://minio:9000" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Access Key</label>
                <Input value={accessKey} onChange={(e) => setAccessKey(e.target.value)} required />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Secret Key</label>
                <Input type="password" value={secretKey} onChange={(e) => setSecretKey(e.target.value)} required />
              </div>
               <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Bucket</label>
                <Input value={bucket} onChange={(e) => setBucket(e.target.value)} required />
              </div>
            </div>
          )}

          <div className="pt-4">
            <Button type="submit">Create Resource</Button>
          </div>
        </form>
      </div>
    </Layout>
  );
};

export default CreateResource;
