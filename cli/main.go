package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

func main() {
	loginUrl := "http://127.0.0.1:5000/api-login"

	// aircraft <command>
	// <company_name> <APi_Key>
	if len(os.Args) != 2 {
		fmt.Println("Command error")
		return
	}

	command := os.Args[0]
	subcommand := os.Args[1]

	if command != "aircraft" ||
		subcommand != "login" {
		fmt.Println("Login error")
	}

	var company string
	fmt.Print("Company Name:")
	fmt.Scanln(&company)

	var apiKey string
	fmt.Print("Api Key:")
	fmt.Scanln(&apiKey)

	loginInfo := map[string]string{
		"company-name": company,
		"api-key":      apiKey,
	}

	jsonData, _ := json.Marshal((loginInfo))

	resp, err := http.Post(
		loginUrl,
		"application/json",
		bytes.NewBuffer(jsonData),
	)

	if err != nil {
		panic(err)
	}

	body, _ := io.ReadAll(resp.Body)
	var data map[string]interface{}
	json.Unmarshal(body, &data)

	token := data["token"].(string)

	saveInfo := map[string]string{
		"company-name": company,
		"token":        token,
	}

	saveData, err := json.Marshal(saveInfo)

	if err != nil {
		panic(err)
	}

	defer resp.Body.Close()

	fmt.Println("Status:", resp.Status)
	home, _ := os.UserHomeDir()
	dir := home + "/.aircraft"
	os.MkdirAll(dir, 0755)

	filePath := dir + "/credentials.json"

	os.WriteFile(filePath, saveData, 0644)

	fmt.Println("Credentials saved:", filePath)
}
