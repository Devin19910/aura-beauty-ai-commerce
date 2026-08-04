'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface WorkflowStatus {
  workflow_status: string;
  progress_percentage: number;
  agents_completed: number;
  total_agents: number;
  current_agent: string | null;
  elapsed_seconds: number | null;
}

interface Summary {
  products_discovered: number;
  suppliers_found: number;
  products_validated: number;
  products_ranked: number;
  quality_score: number;
  approval_rate: number;
}

interface TopProduct {
  product_name: string;
  composite_score: number;
  tier: string;
  final_rank: number;
  roi_information?: {
    annual_roi_pct: number;
    annual_profit: number;
  };
}

interface DashboardData {
  workflow_status: WorkflowStatus;
  summary: Summary;
  top_products: TopProduct[];
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchDashboardData();

    if (autoRefresh) {
      const interval = setInterval(fetchDashboardData, 2000);
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch(`${API_URL}/api/v1/athena/results`);
      if (response.ok) {
        const dashboardData = await response.json();
        setData(dashboardData);
        setLoading(false);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const startWorkflow = async () => {
    setRunning(true);
    try {
      const response = await fetch(`${API_URL}/api/v1/athena/run-workflow`, {
        method: 'POST',
      });
      if (response.ok) {
        const result = await response.json();
        console.log('Workflow started:', result);
        // Fetch data immediately and then keep refreshing
        fetchDashboardData();
      }
    } catch (error) {
      console.error('Error starting workflow:', error);
    } finally {
      setRunning(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8">
        <div className="text-center">
          <div className="text-lg font-semibold">Loading Dashboard...</div>
        </div>
      </div>
    );
  }

  const status = data?.workflow_status || {};
  const summary = data?.summary || {};
  const topProducts = data?.top_products || [];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-600';
      case 'running':
        return 'text-blue-600';
      case 'failed':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  const getTierColor = (tier: string) => {
    if (tier.includes('TIER_1')) return 'bg-green-100 text-green-800';
    if (tier.includes('TIER_2')) return 'bg-blue-100 text-blue-800';
    if (tier.includes('TIER_3')) return 'bg-yellow-100 text-yellow-800';
    return 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-slate-900 mb-2">
            Project Athena Dashboard
          </h1>
          <p className="text-slate-600">
            Real-time monitoring of autonomous product intelligence system
          </p>
        </div>

        {/* Controls */}
        <div className="flex gap-4 mb-8">
          <Button
            onClick={startWorkflow}
            disabled={running}
            className="bg-blue-600 hover:bg-blue-700"
          >
            {running ? 'Running...' : 'Start Workflow'}
          </Button>
          <label className="flex items-center gap-2 text-slate-700">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="rounded"
            />
            Auto-refresh (2s)
          </label>
        </div>

        {/* Workflow Status */}
        <Card className="mb-8 border-slate-200">
          <CardHeader>
            <CardTitle>Workflow Status</CardTitle>
            <CardDescription>Current execution progress</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-slate-700 font-medium">Status:</span>
                <span className={`font-semibold ${getStatusColor(status.workflow_status)}`}>
                  {status.workflow_status?.toUpperCase()}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-700 font-medium">Progress:</span>
                <div className="flex items-center gap-3 flex-1 ml-4">
                  <div className="flex-1 bg-slate-200 rounded-full h-2 overflow-hidden">
                    <div
                      className="bg-blue-600 h-full transition-all duration-300"
                      style={{ width: `${status.progress_percentage || 0}%` }}
                    />
                  </div>
                  <span className="text-slate-700 font-medium min-w-12 text-right">
                    {Math.round(status.progress_percentage || 0)}%
                  </span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-700 font-medium">Agents Completed:</span>
                <span className="font-semibold text-slate-900">
                  {status.agents_completed}/{status.total_agents}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-700 font-medium">Current Agent:</span>
                <span className="font-semibold text-slate-900">
                  {status.current_agent || 'None'}
                </span>
              </div>
              {status.elapsed_seconds !== null && (
                <div className="flex justify-between items-center">
                  <span className="text-slate-700 font-medium">Elapsed Time:</span>
                  <span className="font-semibold text-slate-900">
                    {Math.round(status.elapsed_seconds)}s
                  </span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Summary Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          <Card className="border-slate-200">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-600">
                Products Discovered
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-slate-900">
                {summary.products_discovered || 0}
              </div>
            </CardContent>
          </Card>

          <Card className="border-slate-200">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-600">
                Suppliers Found
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-slate-900">
                {summary.suppliers_found || 0}
              </div>
            </CardContent>
          </Card>

          <Card className="border-slate-200">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-600">
                Products Validated
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-slate-900">
                {summary.products_validated || 0}
              </div>
            </CardContent>
          </Card>

          <Card className="border-slate-200">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-600">
                Products Ranked
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-slate-900">
                {summary.products_ranked || 0}
              </div>
            </CardContent>
          </Card>

          <Card className="border-slate-200">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-600">
                Quality Score
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-slate-900">
                {Math.round(summary.quality_score || 0)}%
              </div>
            </CardContent>
          </Card>

          <Card className="border-slate-200">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-600">
                Approval Rate
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-slate-900">
                {Math.round(summary.approval_rate || 0)}%
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Top Products */}
        <Card className="border-slate-200">
          <CardHeader>
            <CardTitle>Top Recommended Products</CardTitle>
            <CardDescription>Ranked by opportunity score and ROI</CardDescription>
          </CardHeader>
          <CardContent>
            {topProducts.length === 0 ? (
              <div className="text-center py-8 text-slate-500">
                Run workflow to see recommendations
              </div>
            ) : (
              <div className="space-y-4">
                {topProducts.map((product, index) => (
                  <div
                    key={index}
                    className="border border-slate-200 rounded-lg p-4 hover:border-blue-300 hover:bg-slate-50 transition-colors"
                  >
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-lg font-bold text-slate-900">
                            #{product.final_rank}
                          </span>
                          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getTierColor(product.tier)}`}>
                            {product.tier?.replace(/_/g, ' ')}
                          </span>
                        </div>
                        <h3 className="text-slate-900 font-semibold text-lg">
                          {product.product_name}
                        </h3>
                      </div>
                      <div className="text-right">
                        <div className="text-3xl font-bold text-blue-600">
                          {product.composite_score}/100
                        </div>
                        <div className="text-sm text-slate-500">Opportunity Score</div>
                      </div>
                    </div>

                    {product.roi_information && (
                      <div className="grid grid-cols-2 gap-4 mt-3 pt-3 border-t border-slate-200">
                        <div>
                          <div className="text-sm text-slate-600">Annual ROI</div>
                          <div className="text-xl font-bold text-green-600">
                            {Math.round(product.roi_information.annual_roi_pct)}%
                          </div>
                        </div>
                        <div>
                          <div className="text-sm text-slate-600">Annual Profit</div>
                          <div className="text-xl font-bold text-green-600">
                            ${Math.round(product.roi_information.annual_profit).toLocaleString()}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
