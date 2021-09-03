var express = require('express');
var { graphqlHTTP } = require('express-graphql');
var { buildSchema } = require('graphql');

var schema = buildSchema(`
  type User {
    id: String
    name: String
  }

   type Student {
    studentid: String
    studentname: String
    studentdob: String
  }


  type Query {
    usercall(id: String): User
    studentQueryById(studentid: String): Student
    studentQueryByName(studentname: String): Student
    studentQueryByDob(studentdob: String): Student
    othercall: String
  }
`);

// Maps id to User object
var fakeDatabase = {
  'a': {
    id: 'a',
    name: 'alice',
  },
  'b': {
    id: 'b',
    name: 'bob',
  },
  'c': {
    id: 'c',
    name: 'carl',
  },

};

var studentDatabase = {
 'a': {
    studentid: 'b00001',
    studentname: 'alice',
    studentdob: '99'
  },
  'b': {
    studentid: 'b00002',
    studentname: 'bob',
    studentdob: '88'
  },

};

var root = {
  usercall: ({id}) => {
    return fakeDatabase[id]; // mapping to the data
  },

  studentQueryById: ({studentid}) => {
     // send back the data

     var a = studentDatabase['a'];
     if(a.studentid == studentid){
          return a;
     }

     var b = studentDatabase['b'];
     if(b.studentid == studentid){
          return b;
     }


  },
  studentQueryByName: ({studentname}) => {
    var a = studentDatabase['a'];
    if(a.studentname == studentname){
         return a;
    }

    var b = studentDatabase['b'];
    if(b.studentname == studentname){
         return b;
    }
  },
  studentQueryByDob: ({studentdob}) => {
    var a = studentDatabase['a'];
    if(a.studentdob == studentdob){
         return a;
    }

    var b = studentDatabase['b'];
    if(b.studentdob == studentdob){
         return b;
    }
  },


   othercall: ({}) => {
  return 'This is the other call';
  }
};

var app = express();
app.use('/graphql', graphqlHTTP({
  schema: schema,
  rootValue: root,
  graphiql: true,
}));
app.listen(4000);
console.log('Running a GraphQL API server at localhost:4000/graphql');
