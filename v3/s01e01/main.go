package main

import (
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"strconv"

	llm "aidevs/ver3/openai"

	"github.com/gocolly/colly"
	"github.com/joho/godotenv"
)

func main() {

	godotenv.Load("../.env")

	c := colly.NewCollector()

	c.OnHTML("#human-question", func(e *colly.HTMLElement) {
		question := e.Text
		fmt.Print(question)

		answer := llm.Invoke("\n\nAnswer the question by providing only a number eq. 1900,\n\n" + question)
		fmt.Print(answer)

		answerInt, err := strconv.Atoi(answer)
		if err != nil {
			fmt.Print(err.Error())
		}

		data := url.Values{}
		data.Set("username", os.Getenv("XYZ_LOGIN"))
		data.Set("password", os.Getenv("XYZ_PASS"))
		data.Set("answer", strconv.Itoa(answerInt))

		resp, err := http.PostForm("https://xyz.ag3nts.org/", data)
		if err != nil {
			fmt.Print(err.Error())
			return
		}

		defer resp.Body.Close()
		respBody, err := io.ReadAll(resp.Body)
		if err != nil {
			fmt.Print(err.Error())
			return
		}

		fmt.Print(string(respBody))
	})

	c.Visit("https://xyz.ag3nts.org/")
}
