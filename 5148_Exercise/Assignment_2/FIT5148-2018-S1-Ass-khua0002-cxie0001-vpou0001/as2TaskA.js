// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// NOTICE
// Please run as2TaskA.sh shell script for convenience.
// This way the data will be imported before running mongo commands as well.
// $ sh ./as2TaskA.sh
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

// Head
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
print("FIT5148 Assignment 2 - Part A");
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
use fit5148_db;
var fireCreated = db.createCollection("fire");
var climateCreated = db.createCollection("climate");
print("Collections created.");


// Task A.1
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
print("Task A.1");
// mongoimport -d fit5148_db -c climate --type csv --file ClimateData-Part1.csv --headerline
// mongoimport -d fit5148_db -c fire --type csv --file FireData-Part1.csv --headerline
print("Data imported to collections.");


// Task A.2
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
print("Task A.2");
var A2 = db.climate.find({ "Date": "2017-12-15" });
while (A2.hasNext()) printjson(A2.next());


// Task A.3
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
print("Task A.3");
var A3 = db.fire.find(
    { "Surface Temperature (Celcius)": { $gte: 65, $lte: 100 } },
    { _id: 0, "Latitude": 1, "Longitude": 1, "Confidence": 1 }
).sort({ "Confidence": 1 });
while (A3.hasNext()) printjson(A3.next());


// Task A.4
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
print("Task A.4");
var A4 = db.climate.aggregate([
    { $lookup: { from: "fire", localField: "Date", foreignField: "Date", as: "fire" } },
    { $match: { $or: [{ "Date": { $eq: "2017-12-15" } }, { "Date": { $eq: "2017-12-16" } }] } },
    {
        $project: {
            _id: 0,
            "Date": 1,
            Surface_Temperature: "$fire.Surface Temperature (Celcius)", // update: Chuangfu
            "Air Temperature(Celcius)": 1,
            "Relative Humidity": 1,
            "Max Wind Speed": 1
        }
    },
    {$unwind: "$Surface_Temperature"} // update: Chuangfu
]);
while (A4.hasNext()) printjson(A4.next());


// Task A.5
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
print("Task A.5");
var A5 = db.fire.aggregate([
    { $lookup: { from: "climate", localField: "Date", foreignField: "Date", as: "climate" } },
    { $match: { $and: [{ "Confidence": { $gte: 80 } }, { "Confidence": { $lte: 100 } }] } },
    {
        $project: {
            _id: 0,
            "Datetime": 1,
            "Surface Temperature (Celcius)": 1,
            "Confidence": 1,
            Air_Temperature: "$climate.Air Temperature(Celcius)" // update: Chuangfu
        }
    },
    { $unwind: "$Air_Temperature"} // update: Chuangfu
]);
while (A5.hasNext()) printjson(A5.next());

// Task A.6
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
print("Task A.6");
var A6 = db.fire.find(
    {},
    { _id: 0, "Surface Temperature (Celcius)": 1 }
).sort({ "Surface Temperature (Celcius)": -1 }).limit(10);
while (A6.hasNext()) printjson(A6.next());


// Task A.7
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
print("Task A.7");
var A7 = db.fire.aggregate([
    { $group: { _id: "$Date", total: { $sum: 1 } } },
    { $project: { _id: 0, date: "$_id", total: 1 } }
])
while (A7.hasNext()) printjson(A7.next());


// Task A.8
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
print("Task A.8");
var A8 = db.fire.aggregate([
    { $group: { _id: "$Date", average: { $avg: "$Surface Temperature (Celcius)" } } },
    { $project: { _id: 0, date: "$_id", average: 1 } }
])
while (A8.hasNext()) printjson(A8.next());


// Tail
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -");
// if (db.fire.drop() && db.climate.drop()) {
//     print("Collections dropped.");
// }
