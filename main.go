package main

import (
	"bytes"
	"crypto/cipher"
	"crypto/des"
	"database/sql"
	"encoding/json"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/gorilla/context"
	"github.com/gorilla/mux"
	"github.com/gorilla/sessions"
	_ "github.com/lib/pq"
)

var store = sessions.NewCookieStore([]byte(os.Getenv("aHf5FsFd93f3232trfhGbSDW82bHsicL")))

type Config struct {
	SecritCookie string
}

type heKyeST struct {
	key string
}

// User класс пользователя
type User struct {
	ID       int
	Name     string
	Password string
	Admin    bool
	Op       int
	Moder    bool
	Ava      string
	Status   string
	Color    string
}

// LoginUser - авторизация
type LoginUser struct {
	Name     string
	Password string
	SicretKey string
	Success  bool
}

// Type класс раздела
type Type struct {
	ID    int
	Title string
	MinOp int
}

// Theme класс темы 
type Theme struct {
	ID        int
	Title     string
	MiniDop   string
	Date      time.Time
	MinOp     int
	OnlyRead  bool
	CreUserID int
	Fixing    bool
	TypeID    int
	Anon      bool 
}

// Message класс сообщений 
type Message struct {
	ID         int
	TextMsg    []byte
	UserID     int
	ThemeID    int
	PubDate    time.Time
}

// DeshifrMessage - тот-же Message, только TextMsg строковой
type DeshifrMessage struct {
	ID         int
	TextMsg    string
	UserID     int
	ThemeID    int
	PubDate    time.Time
	UserInfo   []User
}

func conn() *sql.DB {
	conn := fmt.Sprint("user=ijvqxpzulogxyt password=c118cf0739abbc357614cb5cb38dc84f8ae08fcc331e20f1725f224270ace732 host=ec2-46-137-79-235.eu-west-1.compute.amazonaws.com port=5432 dbname=d655kmienbsq13 sslmode=require")
	db, err := sql.Open("postgres", conn)

	if err != nil {
		log.Fatal(err)
	}

	return db
}

func JSONread() string {
	file, err := os.Open("config.json")

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(file)

	config := json.NewDecoder(file)
	fmt.Println(config)

	result := new(Config)
	// result.SecritCookie = config["secritCookie"]

	err2 := config.Decode(&result)
	if err2 != nil {
		fmt.Print("Err")
		fmt.Println(err2)
	}
	
	defer file.Close()

	return result.SecritCookie
}

func DesEncryption(key, iv, plainText []byte) ([]byte, error) {

	block, err := des.NewCipher(key)

	if err != nil {
			return nil, err
	}

	blockSize := block.BlockSize()
	origData := PKCS5Padding(plainText, blockSize)
	blockMode := cipher.NewCBCEncrypter(block, iv)
	cryted := make([]byte, len(origData))
	blockMode.CryptBlocks(cryted, origData)
	return cryted, nil
}

func DesDecryption(key, iv, cipherText []byte) ([]byte, error) {

	block, err := des.NewCipher(key)

	if err != nil {
			return nil, err
	}

	blockMode := cipher.NewCBCDecrypter(block, iv)
	origData := make([]byte, len(cipherText))
	blockMode.CryptBlocks(origData, cipherText)
	origData = PKCS5UnPadding(origData)
	fmt.Print(origData, "+\n\n\n+")
	return origData, nil
}

func PKCS5Padding(src []byte, blockSize int) []byte {
	padding := blockSize - len(src)%blockSize
	padtext := bytes.Repeat([]byte{byte(padding)}, padding)
	return append(src, padtext...)
}

func PKCS5UnPadding(src []byte) []byte {
	var result []byte
	var diap int

	length := len(src)
	unpadding := int(src[length-1])
	
	if length - unpadding < 0 {
		diap = (length - unpadding) * -1
	} else {
		diap = length - unpadding
	}

	if diap >= length {
		diap = length-1
	}

	result = src[:diap]
	return result
}                                        

func getUsers(sqlCode string) []User {
	// conn := fmt.Sprint("user=fldyqnxcgmlctw password=d86ddbb94a3059ab90cea9bb58432f1e4150a85bfbd440cd1fa8b9ecd45a8618 host=ec2-54-76-215-139.eu-west-1.compute.amazonaws.com port=5432 dbname=db85a48j30fvr sslmode=require")
	// db, err := sql.Open("postgres", conn)

	// if err != nil {
	// 	log.Fatal(err)
	// }

	db := conn()

	value, err := db.Query(sqlCode)

	if err != nil {
		fmt.Print("Error: ")
		log.Fatal(err)
	}

	Users := []User{}

	for value.Next() {
		u := User{}
		err := value.Scan(&u.ID, &u.Name, &u.Password, &u.Admin, &u.Op, &u.Moder, &u.Ava, &u.Status, &u.Color)

		if err != nil {
			fmt.Println(err)
			continue
		}
		Users = append(Users, u)
	}

	defer db.Close()

	return Users
}

func getTypes(sqlCode string) []Type {
	db := conn()

	value, err := db.Query(sqlCode)

	if err != nil {
		fmt.Print("Error: ")
		log.Fatal(err)
	}

	Types := []Type{}

	for value.Next() {
		t := Type{}
		err := value.Scan(&t.ID, &t.Title, &t.MinOp)

		if err != nil {
			fmt.Println(err)
			continue
		}
		Types = append(Types, t)
	}

	defer db.Close()

	return Types
}

func getThemes(sqlCode string) []Theme {
	db := conn()

	value, err := db.Query(sqlCode)

	if err != nil {
		fmt.Print("Error: ")
		log.Fatal(err)
	}

	Themes := []Theme{}

	for value.Next() {
		t := Theme{}
		err := value.Scan(&t.ID, &t.Title, &t.MiniDop, &t.Date, &t.MinOp, &t.OnlyRead, &t.CreUserID, &t.Fixing, &t.TypeID, &t.Anon)

		if err != nil {
			fmt.Println(err)
			continue
		}
		Themes = append(Themes, t)
	}

	defer db.Close()

	return Themes
}

func getMessages(sqlCode string) []Message {
	db := conn()

	value, err := db.Query(sqlCode)

	if err != nil {
		fmt.Print("Error: ")
		log.Fatal(err)
	}

	Messages := []Message{}

	for value.Next() {
		m := Message{}
		err := value.Scan(&m.ID, &m.TextMsg, &m.UserID, &m.ThemeID, &m.PubDate)

		if err != nil {
			fmt.Println(err)
			continue
		}
		Messages = append(Messages, m)
	}

	defer db.Close()

	return Messages
}


func homePage(w http.ResponseWriter, r *http.Request) {
	Types := getTypes("SELECT * FROM \"Type\"")

	//var ThemeByType map[string]Theme
	// TAT - ThemesAndTypes
	var TAT map[string][]Theme
	TAT = make(map[string][]Theme)

	for i := range Types {
		Themes := getThemes((fmt.Sprintf("SELECT * FROM \"Theme\" WHERE type_id=%d", Types[i].ID)))

		var j string = Types[i].Title
		TAT[j] = Themes
	}
	fmt.Println(TAT)

	tmpl, err := template.ParseFiles("templates/homePage.html", "templates/header.html", "templates/footer.html")
	// for i, value := range TAT {
	// 	fmt.Print(i)
	// 	fmt.Print(":\n")
	// 	for j := range value {
	// 		fmt.Print("   ")
	// 		fmt.Print(value[j])
	// 		fmt.Print("\n")
	// 	}
	// 	fmt.Print("\n")
	// }

	if err != nil {
		fmt.Fprintf(w, err.Error())
	}

	var session *sessions.Session
	session, _ = store.Get(r, "User")

	fmt.Printf("\n\n\n")
	fmt.Println(session.Values["Name"])
	fmt.Printf("\n\n\n")

	tmpl.ExecuteTemplate(w, "index", TAT)
}

func openTheme(w http.ResponseWriter, r *http.Request) {
	Vars := mux.Vars(r)
	w.WriteHeader(http.StatusOK)

	ThemeID := Vars["id"]
	ThemeInfo := getThemes(fmt.Sprintf("SELECT * FROM \"Theme\" WHERE id=%s", ThemeID))[0]
	//WHERE rubric_id=%s;
	Messages := getMessages(fmt.Sprintf("SELECT * FROM \"Message\" WHERE rubric_id=%s", ThemeID))
	DeshifrMessages := []DeshifrMessage{}

	fmt.Println(Messages)
	if Messages != nil {
		var deKey interface{}
		var stringDeKey string
		var sessionKey *sessions.Session

		for i := range Messages {
			fmt.Print(">>>")
			fmt.Println(Messages[i].TextMsg)
			sessionKey, _ = store.Get(r, "drYdvaj29dS2kEy$2wcdsgdsauw")
			deKey = sessionKey.Values["Key"]
			stringDeKey = fmt.Sprintf("%s", deKey)
			fmt.Print(stringDeKey)
			if stringDeKey == "" || len(stringDeKey) != 8 {
				stringDeKey = "keyIdiot"
			}

			byteDeKey := []byte(stringDeKey)
			fmt.Print("\n\n\n")
			fmt.Println(byteDeKey)
			// ivKey := []byte(string(byteDeKey) + strings.Repeat("0", 16))
			// byteDeKey = []byte(string(byteDeKey) + strings.Repeat("0", 16))
			ivKey := byteDeKey
			fmt.Println(string(ivKey))
			fmt.Println(ivKey)
			deMsgText, errDes := DesDecryption(byteDeKey, ivKey, Messages[i].TextMsg)

			if errDes != nil {
				fmt.Fprintf(w, "Error404")
			}
			//deMsgText := byteTextMessages
			fmt.Print("--")

			// if errDe != nil {
			// 	fmt.Print("Err: ")
			// 	log.Fatal(errDe)
			// }

			fmt.Print(">")
			TextMsg := string(deMsgText)
			fmt.Print("\n\n\n>")
			fmt.Println(TextMsg)
			UserInfo := getUsers(fmt.Sprintf("SELECT id, name, password, admin, op, moder, ava, status, color FROM \"User\" WHERE id=%d", Messages[i].UserID))

			Msg := DeshifrMessage{Messages[i].ID, TextMsg, Messages[i].UserID, Messages[i].ThemeID, Messages[i].PubDate, UserInfo}
			DeshifrMessages = append(DeshifrMessages, Msg)
		} 
	}

	// DataTaDM Словарь для хранения Theme и DeshifrMsg, TaMD - Theme and DeshifrMsg

	session, _ := store.Get(r, "User")
	UserName := session.Values["Name"]
	fmt.Print("UserName: ")
	fmt.Println(UserName)
	var data interface{}
	if UserName == nil {
		type DataTaDM struct {
			ThemeInfo Theme
			Messages  []DeshifrMessage
			User      interface{}
		}

		data = DataTaDM{ThemeInfo: ThemeInfo, Messages: DeshifrMessages, User: nil}
		fmt.Println("a")
	} else {
		type UserCookie struct {
			Name interface{}
			OP   interface{}
			ID   interface{}
		}
		type DataTaDM struct {
			ThemeInfo Theme
			Messages  []DeshifrMessage
			User 			UserCookie
		}

		cookieUserName := session.Values["Name"]
		Name := cookieUserName
		OP := session.Values["OP"]

		data = DataTaDM{
			ThemeInfo: ThemeInfo,
			Messages: DeshifrMessages,
			User: UserCookie{
				Name:  Name,
				OP: 	 OP,
				ID:    session.Values["ID"],
			},
		}
		fmt.Println("b")
	}
	fmt.Println(data)
	

	tmpl, err := template.ParseFiles("templates/theme.html", "templates/header.html", "templates/footer.html")

	if err != nil {
		fmt.Fprintf(w, err.Error())
	}

	tmpl.ExecuteTemplate(w, "theme", data)
}

func Login(w http.ResponseWriter, r *http.Request) {
	tmpl, err := template.ParseFiles("templates/login.html", "templates/header.html", "templates/footer.html")

	if err != nil {
		fmt.Fprintf(w, err.Error())
	}
	//fmt.Println(c.Value)

	tmpl.ExecuteTemplate(w, "login", nil)
}

func Loginka(w http.ResponseWriter, r *http.Request) {

	data := LoginUser{
		Name: r.FormValue("Nik"),
		Password: r.FormValue("Pass"),
		SicretKey: r.FormValue("sicretKey"),
	}

	jsonData := JSONread()

	if jsonData == data.SicretKey {
		// tmpl, err := template.ParseFiles("templates/login.html", "templates/theme.html", "templates/homePage.html")
		// if err != nil {
		// 	fmt.Print("Error: ")
		// 	log.Fatal(err)
		// }

		data.Success = true

		type CheckNameAndPassword struct {
			ID int
			OP int
		}

		sqlCode := fmt.Sprintf("SELECT id, op FROM \"User\" WHERE name='%s' AND password='%s';", data.Name, data.Password)
		fmt.Println(sqlCode)

		db := conn()

		User, err := db.Query(sqlCode)

		if err != nil {
			fmt.Println(err)
		}

		CheckUser := []CheckNameAndPassword{}
		for User.Next() {
			u := CheckNameAndPassword{}
			err := User.Scan(&u.ID, &u.OP)
	
			if err != nil {
				fmt.Println(err)
				continue
			}

			CheckUser = append(CheckUser, u)
		}

		fmt.Println(CheckUser)

		if len(CheckUser) == 1 {
			session, _ := store.Get(r, "User")
			session.Values["Name"] = data.Name
			session.Values["OP"] = CheckUser[0].OP
			session.Values["ID"] = CheckUser[0].ID
			err := session.Save(r, w)
			fmt.Print(">>>>")
			fmt.Println(session.Values["Name"])
			fmt.Println(session.Values["OP"])

			if err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}

			defer db.Close()

			http.Redirect(w, r, "/", http.StatusSeeOther)
		} else {
			defer db.Close()

			http.Redirect(w, r, "/login/", http.StatusSeeOther)
		}
	}

	
}

func ClearCookie(w http.ResponseWriter, r *http.Request) {
	session, _ := store.Get(r, "User")
	session.Options.MaxAge = -1
	err := session.Save(r, w)

	if err != nil {
		log.Fatal("failed to delete session", err)
	}

	session2, _ := store.Get(r, "drYdvaj29dS2kEy$2wcdsgdsauw")
	session2.Options.MaxAge = -1
	err2 := session2.Save(r, w)

	if err2 != nil {
		log.Fatal("failed to delete session", err2)
	}

	http.Redirect(w, r, "/", http.StatusSeeOther)
}

func heKey(w http.ResponseWriter, r *http.Request) {

	key := r.FormValue("Key")

	session, _ := store.Get(r, "drYdvaj29dS2kEy$2wcdsgdsauw")
	session.Values["Key"] = key
	err := session.Save(r, w)
	fmt.Println(session.Values["Key"])

	if err != nil {
		log.Fatal("failed to delete session", err)
	}

	http.Redirect(w, r, r.Header.Get("Referer"), http.StatusSeeOther)
}

func AddMsg(w http.ResponseWriter, r *http.Request) {
	userID := r.FormValue("userID")
	themeID := r.FormValue("themeID")
	msgText := r.FormValue("MsgText")
	fmt.Println(msgText)

	if len(msgText) % 8 != 0 {
		for len(msgText) % 8 != 0 {
			msgText = msgText + " "
		}
	}

	fmt.Println(fmt.Sprintf("\"%s\"", msgText))

	session, _ := store.Get(r, "drYdvaj29dS2kEy$2wcdsgdsauw")
	fmt.Println("b")
	key := session.Values["Key"]
	keyHe := fmt.Sprintf("%s", key)
	if keyHe == "" || len(keyHe) / 8 != 1 {
		keyHe = "keyIdiot"
	}
	keyShifr := []byte(keyHe)
	fmt.Println("c")
	fmt.Println(keyHe)

	textMsg := []byte(msgText)

	// ivKey := []byte(string(keyShifr) + strings.Repeat("0", 16))
	// keyShifr = []byte(string(keyShifr) + strings.Repeat("0", 16))
	ivKey := keyShifr
	fmt.Println(len(ivKey))
	text, err := DesEncryption(keyShifr, ivKey, textMsg)
	//SStextMsg := string(text)
	if err != nil {
		log.Fatal(err)
	}

	// var listUint8 []uint8

	// for i := text {
	// 	listUIN8 = append(listUIN8, text[i])
	// }
	// fmt.Println(listUIN8)
	//textMessages := string(text)
	//fmt.Println(textMessages)

	db := conn()
	t := time.Now()

	intUserID, errUserID := strconv.Atoi(userID)
	if errUserID != nil {
		log.Fatal(errUserID)
	}

	intThemeID, errThemeID := strconv.Atoi(themeID)
	if errThemeID != nil {
		log.Fatal(errThemeID)
	}

	fmt.Println(intThemeID)
	fmt.Println(intUserID)
	fmt.Println(text)
	fmt.Println(string(text))

	//codyUTF, errSqlUTF := db.Query("SET client_encoding = 'UTF8';")
	//(SELECT MAX(id) FROM \"Message\")+
	db.Exec("INSERT INTO \"Message\"(id, text, user_id, rubric_id, pub_date) VALUES ((SELECT MAX(id) FROm \"Message\")+1, $1, $2, $3, $4)", text, intUserID, intThemeID, t.Format(time.RFC3339))
	// (SELECT MAX(id) FROM \"Message\")+
	// Vars := mux.Vars(r)
	// w.WriteHeader(http.StatusOK)

	// redic := Vars["redic"]
	defer db.Close()

	defer http.Redirect(w, r, r.Header.Get("Referer"), http.StatusSeeOther)
}

func handleRequest() {
	rtr := mux.NewRouter()
	rtr.HandleFunc("/", homePage).Methods("GET")
	rtr.HandleFunc("/theme/{id:[0-9]+}/", openTheme).Methods("GET")
	rtr.HandleFunc("/login/", Login).Methods("GET")
	rtr.HandleFunc("/authtorization/", Loginka).Methods("POST")
	rtr.HandleFunc("/clearCookie/", ClearCookie).Methods("GET")
	rtr.HandleFunc("/addMsg/", AddMsg).Methods("POST")
	rtr.HandleFunc("/heKey/", heKey).Methods("POST")
	
	http.Handle("/", rtr)
	http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("./static/"))))
	
	port := os.Getenv("PORT")
	if port == "" {
		port = "9000"
	}
	http.ListenAndServe(":" + port, context.ClearHandler(http.DefaultServeMux))
	// http.ListenAndServe(":8000", nil)
}

func main() {
	handleRequest()
}
