"use strict";
const AWS = require("aws-sdk");
AWS.config.update({ region: "eu-west-1" });

exports.handler = function (event, context, callback) {
  const ddb = new AWS.DynamoDB({ apiVersion: "2012-10-08" });
  const documentClient = new AWS.DynamoDB.DocumentClient({
    // will marshall/unmarshall object
    region: "eu-west-1",
  });
  const params = {
    TableName: "Users",
    Key: {
      //   id: {
      //     S: "12345",
      //   },
      id: "12345",
    },
  };

  //   ddb.getItem(params, (err, data) => {
  //     if (err) {
  //       console.log(err);
  //     }
  //     console.log(data);
  //   });
  documentClient.get(params, (err, data) => {
    if (err) {
      console.log(err);
    }
    console.log(data);
  });
};
