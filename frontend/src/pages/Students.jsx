import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Plus, Search, Filter, MoreHorizontal, Edit, Eye } from 'lucide-react';

const Students = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedClass, setSelectedClass] = useState('all');

  // Mock data - replace with actual API calls
  const students = [
    {
      id: '1',
      name: 'Alice Johnson',
      studentId: 'STU001',
      class: '10',
      section: 'A',
      rollNumber: '001',
      status: 'active',
      feeStatus: 'paid',
      contactNumber: '+1 234 567 8901',
      email: 'alice.johnson@email.com'
    },
    {
      id: '2',
      name: 'Bob Smith',
      studentId: 'STU002',
      class: '10',
      section: 'A',
      rollNumber: '002',
      status: 'active',
      feeStatus: 'pending',
      contactNumber: '+1 234 567 8902',
      email: 'bob.smith@email.com'
    },
    {
      id: '3',
      name: 'Charlie Brown',
      studentId: 'STU003',
      class: '9',
      section: 'B',
      rollNumber: '003',
      status: 'active',
      feeStatus: 'overdue',
      contactNumber: '+1 234 567 8903',
      email: 'charlie.brown@email.com'
    },
    {
      id: '4',
      name: 'Diana Wilson',
      studentId: 'STU004',
      class: '11',
      section: 'A',
      rollNumber: '004',
      status: 'active',
      feeStatus: 'paid',
      contactNumber: '+1 234 567 8904',
      email: 'diana.wilson@email.com'
    }
  ];

  const filteredStudents = students.filter(student => {
    const matchesSearch = student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         student.studentId.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesClass = selectedClass === 'all' || student.class === selectedClass;
    return matchesSearch && matchesClass;
  });

  const getStatusBadge = (status) => {
    const variants = {
      active: 'bg-green-100 text-green-800',
      inactive: 'bg-gray-100 text-gray-800'
    };
    return variants[status] || variants.active;
  };

  const getFeeStatusBadge = (status) => {
    const variants = {
      paid: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      overdue: 'bg-red-100 text-red-800'
    };
    return variants[status] || variants.pending;
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Students</h1>
          <p className="text-gray-600">Manage your school's student records</p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700">
          <Plus className="w-4 h-4 mr-2" />
          Add Student
        </Button>
      </div>

      {/* Filters */}
      <Card className="shadow-soft border-0">
        <CardContent className="p-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  placeholder="Search by name or student ID..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <select
                value={selectedClass}
                onChange={(e) => setSelectedClass(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Classes</option>
                <option value="9">Class 9</option>
                <option value="10">Class 10</option>
                <option value="11">Class 11</option>
                <option value="12">Class 12</option>
              </select>
              <Button variant="outline">
                <Filter className="w-4 h-4 mr-2" />
                More Filters
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Students Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredStudents.map((student) => (
          <Card key={student.id} className="shadow-soft border-0 hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-lg">{student.name}</CardTitle>
                  <CardDescription>ID: {student.studentId}</CardDescription>
                </div>
                <Button variant="ghost" size="sm">
                  <MoreHorizontal className="w-4 h-4" />
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Class:</span>
                  <span className="font-medium">{student.class}-{student.section}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Roll No:</span>
                  <span className="font-medium">{student.rollNumber}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Status:</span>
                  <Badge className={getStatusBadge(student.status)}>
                    {student.status}
                  </Badge>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Fee Status:</span>
                  <Badge className={getFeeStatusBadge(student.feeStatus)}>
                    {student.feeStatus}
                  </Badge>
                </div>
                
                <div className="pt-3 border-t border-gray-100">
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" className="flex-1">
                      <Eye className="w-4 h-4 mr-1" />
                      View
                    </Button>
                    <Button variant="outline" size="sm" className="flex-1">
                      <Edit className="w-4 h-4 mr-1" />
                      Edit
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Stats Summary */}
      <Card className="shadow-soft border-0">
        <CardHeader>
          <CardTitle>Student Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{students.length}</p>
              <p className="text-sm text-gray-600">Total Students</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">
                {students.filter(s => s.status === 'active').length}
              </p>
              <p className="text-sm text-gray-600">Active</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-yellow-600">
                {students.filter(s => s.feeStatus === 'pending').length}
              </p>
              <p className="text-sm text-gray-600">Fee Pending</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-red-600">
                {students.filter(s => s.feeStatus === 'overdue').length}
              </p>
              <p className="text-sm text-gray-600">Fee Overdue</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Students;