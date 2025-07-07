import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, DollarSign, Calendar, BookOpen, TrendingUp, TrendingDown } from 'lucide-react';

const Dashboard = () => {
  // Mock data - replace with actual API calls
  const stats = [
    {
      title: 'Total Students',
      value: '1,248',
      change: '+12%',
      trend: 'up',
      icon: Users,
      color: 'text-blue-600'
    },
    {
      title: 'Fee Collection',
      value: '$142,580',
      change: '+8%',
      trend: 'up',
      icon: DollarSign,
      color: 'text-green-600'
    },
    {
      title: 'Attendance Today',
      value: '94.2%',
      change: '-2%',
      trend: 'down',
      icon: Calendar,
      color: 'text-orange-600'
    },
    {
      title: 'Active Classes',
      value: '28',
      change: '+3%',
      trend: 'up',
      icon: BookOpen,
      color: 'text-purple-600'
    }
  ];

  const recentActivities = [
    { type: 'student', message: 'New student Emma Johnson enrolled in Grade 10-A', time: '2 hours ago' },
    { type: 'fee', message: 'Fee payment of $500 received from John Smith', time: '4 hours ago' },
    { type: 'attendance', message: 'Grade 9-B marked present - 28/30 students', time: '6 hours ago' },
    { type: 'result', message: 'Mathematics test results uploaded for Grade 8-C', time: '1 day ago' },
  ];

  return (
    <div className="p-6 space-y-6">
      {/* Welcome Section */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Welcome back! Here's what's happening at your school today.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <Card key={index} className="shadow-soft border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-1">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  <div className="flex items-center mt-2">
                    {stat.trend === 'up' ? (
                      <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
                    ) : (
                      <TrendingDown className="w-4 h-4 text-red-500 mr-1" />
                    )}
                    <span className={`text-sm font-medium ${
                      stat.trend === 'up' ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {stat.change}
                    </span>
                    <span className="text-sm text-gray-500 ml-1">vs last month</span>
                  </div>
                </div>
                <div className={`p-3 rounded-lg bg-gray-50`}>
                  <stat.icon className={`w-6 h-6 ${stat.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activities */}
        <Card className="lg:col-span-2 shadow-soft border-0">
          <CardHeader>
            <CardTitle>Recent Activities</CardTitle>
            <CardDescription>Latest updates from your school</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivities.map((activity, index) => (
                <div key={index} className="flex items-start gap-4 p-4 rounded-lg bg-gray-50">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-900 font-medium">{activity.message}</p>
                    <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card className="shadow-soft border-0">
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Common tasks</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <button className="w-full p-4 text-left rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                <div className="flex items-center gap-3">
                  <Users className="w-5 h-5 text-blue-600" />
                  <div>
                    <p className="font-medium text-gray-900">Add New Student</p>
                    <p className="text-sm text-gray-500">Register a new student</p>
                  </div>
                </div>
              </button>
              
              <button className="w-full p-4 text-left rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                <div className="flex items-center gap-3">
                  <Calendar className="w-5 h-5 text-green-600" />
                  <div>
                    <p className="font-medium text-gray-900">Mark Attendance</p>
                    <p className="text-sm text-gray-500">Today's attendance</p>
                  </div>
                </div>
              </button>
              
              <button className="w-full p-4 text-left rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                <div className="flex items-center gap-3">
                  <DollarSign className="w-5 h-5 text-orange-600" />
                  <div>
                    <p className="font-medium text-gray-900">Record Payment</p>
                    <p className="text-sm text-gray-500">Update fee status</p>
                  </div>
                </div>
              </button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;