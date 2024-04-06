package main

import (
	"context"
	"log"
	"net/http"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type LegoSet struct {
	Theme         string  `bson:"theme"`
	Name          string  `bson:"name"`
	SetNumber     string  `bson:"set_number"`
	Pieces        int     `bson:"pieces"`
	Minifigs      int     `bson:"minifigs"`
	Price         float64 `bson:"price"`
	PricePerPiece float64 `bson:"price_per_piece"`
	Year          int     `bson:"year"`
	Packaging     string  `bson:"packaging"`
}

var collection *mongo.Collection

func main() {
	client, err := mongo.Connect(context.TODO(), options.Client().ApplyURI("mongodb://localhost:27017"))
	if err != nil {
		log.Fatal(err)
	}

	collection = client.Database("lego_sets").Collection("sets")

	router := gin.Default()
	router.GET("/sets", getAllSets)
	router.GET("/set/:setNumber", getSetByNumber)
	router.GET("/sets/filter", filterSets)

	router.Run("localhost:8080")
}

func getAllSets(c *gin.Context) {
	cursor, err := collection.Find(context.TODO(), bson.D{})
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	defer cursor.Close(context.TODO())

	var sets []LegoSet
	if err = cursor.All(context.TODO(), &sets); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, sets)
}

func getSetByNumber(c *gin.Context) {
	setNumber := c.Param("setNumber")

	var set LegoSet
	err := collection.FindOne(context.TODO(), bson.M{"set_number": setNumber}).Decode(&set)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Set not found"})
		return
	}

	c.JSON(http.StatusOK, set)
}

func filterSets(c *gin.Context) {
	filter := bson.D{}

	theme := c.Query("theme")
	if theme != "" {
		filter = append(filter, bson.E{Key: "theme", Value: strings.ToLower(theme)})
	}

	minPieces, _ := strconv.Atoi(c.Query("minPieces"))
	if minPieces > 0 {
		filter = append(filter, bson.E{Key: "pieces", Value: bson.D{{Key: "$gte", Value: minPieces}}})
	}

	maxPieces, _ := strconv.Atoi(c.Query("maxPieces"))
	if maxPieces > 0 {
		filter = append(filter, bson.E{Key: "pieces", Value: bson.D{{Key: "$lte", Value: maxPieces}}})
	}

	minMinifigs, _ := strconv.Atoi(c.Query("minMinifigs"))
	if minMinifigs > 0 {
		filter = append(filter, bson.E{Key: "minifigs", Value: bson.D{{Key: "$gte", Value: minMinifigs}}})
	}

	maxMinifigs, _ := strconv.Atoi(c.Query("maxMinifigs"))
	if maxMinifigs > 0 {
		filter = append(filter, bson.E{Key: "minifigs", Value: bson.D{{Key: "$lte", Value: maxMinifigs}}})
	}

	minPrice, _ := strconv.ParseFloat(c.Query("minPrice"), 64)
	if minPrice > 0 {
		filter = append(filter, bson.E{Key: "price", Value: bson.D{{Key: "$gte", Value: minPrice}}})
	}

	maxPrice, _ := strconv.ParseFloat(c.Query("maxPrice"), 64)
	if maxPrice > 0 {
		filter = append(filter, bson.E{Key: "price", Value: bson.D{{Key: "$lte", Value: maxPrice}}})
	}

	cursor, err := collection.Find(context.TODO(), filter)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	defer cursor.Close(context.TODO())

	var sets []LegoSet
	if err = cursor.All(context.TODO(), &sets); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, sets)
}
