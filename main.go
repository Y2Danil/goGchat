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
	"sort"
	"strconv"
	"time"

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

type OPuser struct {
	OP int16
}

type RegisterStruct struct {
	Nick string
	Pass1 string
	Pass2 string
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
	ID        int64
	Title     string
	MiniDop   string
	Date      time.Time
	MinOp     int16
	OnlyRead  bool
	CreUserID int64
	Fixing    bool
	TypeID    int16
	Anon      bool 
}

type ThemeTitleAndMinDopAndID struct {
	Title   string
	MiniDop string
	ID      int64
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
		if length != 0 {
			diap = length-1
		} else {
			diap = 1
		}
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

func OpenType(w http.ResponseWriter, r *http.Request) {
	type StructOpenType struct {
		Title   string
		Themes []ThemeTitleAndMinDopAndID
	}

	var userOP interface{}
	var data = StructOpenType{}

	session, errSession := store.Get(r, "User")

	if session != nil && errSession == nil {
		userOP = session.Values["OP"]
	} else {
		userOP = 0
	}

	vars := mux.Vars(r)
	w.WriteHeader(http.StatusOK)

	typeID := vars["id"]

	db := conn()

	Type, errThemeSQL := db.Query("SELECT min_op, title FROM \"Type\" WHERE id=$1", typeID)

	if errThemeSQL != nil {
		fmt.Fprintf(w, "Error404")
	}

	type ThemeMinOPandTitle struct {
		MinOp int64
		Title string
	}

	themeMinOp := ThemeMinOPandTitle{} 

	for Type.Next() {
		Type.Scan(&themeMinOp.MinOp, &themeMinOp.Title)
	}

	data.Title = themeMinOp.Title

	STRuserOP := fmt.Sprintf("%s", userOP)
	int64userOp, _ := strconv.Atoi(STRuserOP)

	

	if themeMinOp.MinOp <= int64(int64userOp) {
		typeThemes, errThemeSQL := db.Query("SELECT title, mini_dop, id FROM \"Theme\" WHERE type_id=$1", typeID)

		if errThemeSQL != nil {
			fmt.Fprintf(w, "Error404")
		}

		var themeInType = []ThemeTitleAndMinDopAndID{}

		for typeThemes.Next() {
			t := ThemeTitleAndMinDopAndID{}
			typeThemes.Scan(&t.Title, &t.MiniDop, &t.ID)

			themeInType = append(themeInType, t)
		}

		data.Themes = themeInType

		tmpl, err := template.ParseFiles("templates/type.html", "templates/header.html", "templates/footer.html")

		if err != nil {
			fmt.Fprintf(w, "Error404")
		}

		defer db.Close()

		tmpl.ExecuteTemplate(w, "type", data)
	} else {
		defer db.Close()

		defer http.Redirect(w, r, "/", http.StatusSeeOther)
	}
}

type TypeTitleAndID struct {
	Title string
	ID 		int
}

func homePage(w http.ResponseWriter, r *http.Request) {
	Types := getTypes("SELECT * FROM \"Type\"")

	//var ThemeByType map[string]Theme
	// TAT - ThemesAndTypes
	var TAT map[TypeTitleAndID][]Theme
	TAT = make(map[TypeTitleAndID][]Theme)

	for i := range Types {
		Themes := getThemes((fmt.Sprintf("SELECT * FROM \"Theme\" WHERE type_id=%d AND fixing=TRUE", Types[i].ID)))

		j := TypeTitleAndID{
			Title: Types[i].Title,
			ID: Types[i].ID, 
		}
		TAT[j] = Themes
	}
	fmt.Println(TAT)

	tmpl, err := template.ParseFiles("templates/homePage.html", "templates/header.html", "templates/footer.html")

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

type DataTaDM struct {
	ThemeInfo Theme
	Messages  []DeshifrMessage
	User      interface{}
}

func openTheme(w http.ResponseWriter, r *http.Request) {
	Vars := mux.Vars(r)
	w.WriteHeader(http.StatusOK)

	ThemeID := Vars["id"]
	ThemeInfo := getThemes(fmt.Sprintf("SELECT * FROM \"Theme\" WHERE id=%s", ThemeID))[0]
	//WHERE rubric_id=%s;
	Messages := getMessages(fmt.Sprintf("SELECT * FROM \"Message\" WHERE rubric_id=%s", ThemeID))
	DeshifrMessages := []DeshifrMessage{}
	userSession, errUserSession := store.Get(r, "User")

	if errUserSession != nil {
		fmt.Fprintf(w, "Error404")
	}

	var user *sql.Rows
	op := OPuser{}
	var dbErr error
	if userSession != nil {
		db := conn()
		userID := userSession.Values["ID"]

		user, dbErr = db.Query("SELECT OP FROM \"User\" WHERE id=$1", userID)

		if dbErr != nil {
			fmt.Fprintf(w, "Error404")
		}

		for user.Next() {
			err := user.Scan(&op.OP)

			if err != nil {
				fmt.Fprintf(w, "Error404")
			}
		}

		fmt.Println(op)

		defer db.Close()
	} else {
		op = OPuser{OP: 0}
	}

	if op.OP >= ThemeInfo.MinOp {
		if Messages != nil {
			var deKey interface{}
			var stringDeKey string
			var sessionKey *sessions.Session

			if ThemeInfo.Anon == true {

			for i := range Messages {
				sessionKey, _ = store.Get(r, "drYdvaj29dS2kEy$2wcdsgdsauw")
				deKey = sessionKey.Values["Key"]
				stringDeKey = fmt.Sprintf("%s", deKey)
				
				if stringDeKey == "" || len(stringDeKey) != 8 {
					stringDeKey = "keyIdiot"
				}

				byteDeKey := []byte(stringDeKey)
				
				ivKey := byteDeKey
				deMsgText, errDes := DesDecryption(byteDeKey, ivKey, Messages[i].TextMsg)

				if errDes != nil {
					fmt.Fprintf(w, "Error404")
				}

				TextMsg := string(deMsgText)
				UserInfo := getUsers(fmt.Sprintf("SELECT id, name, password, admin, op, moder, ava, status, color FROM \"User\" WHERE id=%d", Messages[i].UserID))

				Msg := DeshifrMessage{Messages[i].ID, TextMsg, Messages[i].UserID, Messages[i].ThemeID, Messages[i].PubDate, UserInfo}
				DeshifrMessages = append(DeshifrMessages, Msg)
			} 
			} else {
				for i := range Messages {
					deMsgText := string(Messages[i].TextMsg)

					TextMsg := string(deMsgText)
					UserInfo := getUsers(fmt.Sprintf("SELECT id, name, password, admin, op, moder, ava, status, color FROM \"User\" WHERE id=%d", Messages[i].UserID))

					Msg := DeshifrMessage{Messages[i].ID, TextMsg, Messages[i].UserID, Messages[i].ThemeID, Messages[i].PubDate, UserInfo}
					DeshifrMessages = append(DeshifrMessages, Msg)
				}
			}
		}

		// DataTaDM Словарь для хранения Theme и DeshifrMsg, TaMD - Theme and DeshifrMsg

		session, _ := store.Get(r, "User")
		UserName := session.Values["Name"]
		fmt.Print("UserName: ")
		fmt.Println(UserName)
		var data = DataTaDM{}
		if UserName == nil {
			data = DataTaDM{ThemeInfo: ThemeInfo, Messages: DeshifrMessages, User: nil}
		} else {
			type UserCookie struct {
				Name interface{}
				OP   interface{}
				ID   interface{}
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

		sort.Slice(data.Messages, func(i, j int) bool {return data.Messages[i].ID < data.Messages[j].ID})
		tmpl.ExecuteTemplate(w, "theme", data)
	}	else {
		var url string = "/"
		http.Redirect(w, r, url, http.StatusSeeOther)
	}
}

func Register(w http.ResponseWriter, r *http.Request) {
	tmpl, err := template.ParseFiles("templates/register.html", "templates/header.html", "templates/footer.html")

	if err != nil {
		fmt.Fprintf(w, "Error404")
	}

	tmpl.ExecuteTemplate(w, "register", nil)
}

func CreateAcc(w http.ResponseWriter, r *http.Request) {
	var data = RegisterStruct{
		Nick: r.FormValue("nick"),
		Pass1: r.FormValue("pass1"),
		Pass2: r.FormValue("pass2"),
	}

	if data.Pass1 == data.Pass2 {
		userList := getUsers("SELECT name, password FROM \"User\"")

		var checkUser bool = false

		for i := range userList {
			if userList[i].Name == data.Nick {
				checkUser = true
				break
			}
		}

		if !checkUser {
			db := conn()

			_, DBerr := db.Exec("insert into \"User\" VALUES ((SELECT MAX(id) FROM \"User\")+1, $1, $2, false, 0, false, 'default_ava.jpg', 'Новый пользователь', '#888', false, null);", data.Nick, data.Pass2)

			if DBerr != nil {
				fmt.Fprintf(w, "Error404")

				defer db.Close()

				defer http.Redirect(w, r, "/register/", http.StatusSeeOther)
			} else {
				defer db.Close()

				defer http.Redirect(w, r, "/login/", http.StatusSeeOther)
			}
		}
	}
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

			defer http.Redirect(w, r, "/", http.StatusSeeOther)
		} else {
			defer db.Close()

			defer http.Redirect(w, r, "/login/", http.StatusSeeOther)
		}
	}
}

func ClearCookie(w http.ResponseWriter, r *http.Request) {
	session2, _ := store.Get(r, "drYdvaj29dS2kEy$2wcdsgdsauw")
	session2.Options.MaxAge = -1
	err2 := session2.Save(r, w)

	if err2 != nil {
		log.Fatal("failed to delete session", err2)
	}

	session, _ := store.Get(r, "User")
	session.Options.MaxAge = -1
	err := session.Save(r, w)

	if err != nil {
		log.Fatal("failed to delete session", err)
	}

	defer http.Redirect(w, r, "/", http.StatusSeeOther)
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

	db := conn()

	themeInfo, errSQL := db.Query("SELECT anon FROM \"Theme\" WHERE id=$1", themeID)

	if errSQL != nil {
		fmt.Fprintf(w, "Error404")
	}

	type ThemeAnon struct {
		Anon bool
	}

	themeAN := ThemeAnon{}

	for themeInfo.Next() {
		err := themeInfo.Scan(&themeAN.Anon)

		if err != nil {
			fmt.Fprintf(w, "Error404")
		}
	}

	var text []byte
	var err error
	if themeAN.Anon == true {
		if len(msgText) % 8 != 0 {
			for len(msgText) % 8 != 0 {
				msgText = msgText + " "
			}
		}

		session, _ := store.Get(r, "drYdvaj29dS2kEy$2wcdsgdsauw")
		key := session.Values["Key"]
		keyHe := fmt.Sprintf("%s", key)

		if keyHe == "" || len(keyHe) / 8 != 1 {
			keyHe = "keyIdiot"
		}

		keyShifr := []byte(keyHe)

		textMsg := []byte(msgText)

		ivKey := keyShifr
		text, err = DesEncryption(keyShifr, ivKey, textMsg)
		
		if err != nil {
			log.Fatal(err)
		}
	} else {
		text = []byte(msgText)
	}

	t := time.Now()

	intUserID, errUserID := strconv.Atoi(userID)
	if errUserID != nil {
		log.Fatal(errUserID)
	}

	intThemeID, errThemeID := strconv.Atoi(themeID)
	if errThemeID != nil {
		log.Fatal(errThemeID)
	}

	db.Exec("INSERT INTO \"Message\"(id, text, user_id, rubric_id, pub_date) VALUES ((SELECT MAX(id) FROm \"Message\")+1, $1, $2, $3, $4)", text, intUserID, intThemeID, t.Format(time.RFC3339))
	
	defer db.Close()

	defer http.Redirect(w, r, r.Header.Get("Referer"), http.StatusSeeOther)
}

func handleRequest() {
	rtr := mux.NewRouter()
	rtr.HandleFunc("/", homePage).Methods("GET")
	rtr.HandleFunc("/{id:[0-9]+}/", OpenType).Methods("GET")
	rtr.HandleFunc("/theme/{id:[0-9]+}/", openTheme).Methods("GET")
	rtr.HandleFunc("/register/", Register).Methods("GET")
	rtr.HandleFunc("/createAcc/", CreateAcc).Methods("POST")
	rtr.HandleFunc("/login/", Login).Methods("GET")
	rtr.HandleFunc("/authtorization/", Loginka).Methods("POST")
	rtr.HandleFunc("/clearCookie/", ClearCookie).Methods("GET")
	rtr.HandleFunc("/addMsg/", AddMsg).Methods("POST")
	rtr.HandleFunc("/heKey/", heKey).Methods("POST")
	
	http.Handle("/", rtr)
	http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("./static/"))))
	// HAHAH Danil перешел с питона на голэнг --
	// port := os.Getenv("PORT")
	// if port == "" {
	// 	port = "9000"
	// }
	// http.ListenAndServe(":" + port, context.ClearHandler(http.DefaultServeMux))
	http.ListenAndServe(":8000", nil)
}

func main() {
	handleRequest()
}
