package client

import (
	"bytes"
	"crypto/tls"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
)

const (
	login        = "/api/v1/login"
	logout       = "/api/v1/logout"
	active       = "/api/v1/active"
	getUsers     = "/api/v1/auth/users"
	getRoles     = "/api/v1/auth/roles"
	addUser      = "/api/v1/auth/adduser"
	addRole      = "/api/v1/auth/addrole"
	deleteRole   = "/api/v1/auth/delrole"
	modUser      = "/api/v1/auth/user/"
	changePass   = "/api/v1/auth/password/"
	modRole      = "/api/v1/auth/role/"
	grantRole    = "/api/v1/auth/grant"
	revokeRole   = "/api/v1/auth/revoke"
	apiKeyHeader = "X-Api-Key"
)

func (s *SynapseClient) Login(username string, password string) error {
	bodyJson := map[string]string{
		"user":   username,
		"passwd": password,
	}
	http.DefaultTransport.(*http.Transport).TLSClientConfig = &tls.Config{InsecureSkipVerify: true}
	bodyJsonMarshal, _ := json.Marshal(bodyJson)

	bodyBuf := bytes.NewBuffer(bodyJsonMarshal)

	loginString := fmt.Sprintf("https://%s:%s%s", s.Host, s.Port, login)

	resp, err := s.HttpClient.Post(loginString, "application/json", bodyBuf)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	s.AuthCookie = resp.Header.Get("Set-Cookie")
	s.BaseRequest.Header = make(http.Header)
	s.BaseRequest.Header.Add("Cookie", s.AuthCookie)

	gm := GenericMessage{}

	bodyBytes, err := io.ReadAll(resp.Body)

	err = json.Unmarshal(bodyBytes, &gm)

	if gm.Status != "ok" || err != nil {
		errorMessage := ErrorMessage{}
		err = json.Unmarshal(bodyBytes, &errorMessage)
		return fmt.Errorf("login failed: %s", errorMessage.Mesg)
	}

	return nil
}

func (s *SynapseClient) Logout() error {
	logoutString := fmt.Sprintf("https://%s:%s%s", s.Host, s.Port, logout)
	req, err := http.NewRequest("GET", logoutString, nil)
	if err != nil {
		return err
	}
	req.Header.Add("Cookie", s.AuthCookie)
	resp, err := s.HttpClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)

	if err != nil {
		return err
	}
	genericMessage := GenericMessage{}
	err = json.Unmarshal(bodyBytes, &genericMessage)

	if err != nil {
		return err
	}

	return nil
}

func (s *SynapseClient) GetActive() error {
	activeString := fmt.Sprintf("https://%s:%s%s", s.Host, s.Port, active)
	activeUrl, err := url.Parse(activeString)
	if err != nil {
		return err
	}
	newReq := s.BaseRequest
	newReq.Method = "GET"
	newReq.URL = activeUrl
	resp, err := s.HttpClient.Do(newReq)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)

	if err != nil {
		return err
	}
	isActive := Active{}
	err = json.Unmarshal(bodyBytes, &isActive)

	return nil
}

func (s *SynapseClient) GetUsers() (Users, error) {
	usersString := fmt.Sprintf("https://%s:%s%s", s.Host, s.Port, getUsers)
	req, err := http.NewRequest("GET", usersString, nil)
	if err != nil {
		return Users{}, err
	}
	req.Header.Add("Cookie", s.AuthCookie)
	resp, err := s.HttpClient.Do(req)
	if err != nil {
		return Users{}, err
	}
	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)

	if err != nil {
		return Users{}, err
	}

	bodyJson := Users{}

	err = json.Unmarshal(bodyBytes, &bodyJson)

	return bodyJson, nil
}

func (s *SynapseClient) GetRoles() (Roles, error) {
	rolesString := fmt.Sprintf("https://%s:%s%s", s.Host, s.Port, getRoles)
	req, err := http.NewRequest("GET", rolesString, nil)
	if err != nil {
		return Roles{}, err
	}
	req.Header.Add("Cookie", s.AuthCookie)
	resp, err := s.HttpClient.Do(req)
	if err != nil {
		return Roles{}, err
	}
	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)

	if err != nil {
		return Roles{}, err
	}

	bodyJson := Roles{}

	err = json.Unmarshal(bodyBytes, &bodyJson)

	return bodyJson, nil
}

func (s *SynapseClient) AddUser(username string) (GenericMessage, error) {
	addUserString := fmt.Sprintf("https://%s:%s%s", s.Host, s.Port, addUser)
	bodyJson := map[string]string{
		"name": username,
	}
	bodyJsonMarshal, _ := json.Marshal(bodyJson)

	bodyBuf := bytes.NewBuffer(bodyJsonMarshal)

	req, err := http.NewRequest("POST", addUserString, bodyBuf)
	if err != nil {
		return GenericMessage{}, err
	}
	req.Header.Add("Cookie", s.AuthCookie)
	resp, err := s.HttpClient.Do(req)
	if err != nil {
		return GenericMessage{}, err
	}
	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)

	if err != nil {
		return GenericMessage{}, err
	}

	genericMessage := GenericMessage{}
	err = json.Unmarshal(bodyBytes, &genericMessage)

	if err != nil {
		return GenericMessage{}, err
	}

	return genericMessage, nil
}

func (s *SynapseClient) AddRole(roleName string) (GenericMessage, error) {
	addRoleString := fmt.Sprintf("https://%s:%s%s", s.Host, s.Port, addRole)
	bodyJson := map[string]string{
		"name": roleName,
	}
	bodyJsonMarshal, _ := json.Marshal(bodyJson)

	bodyBuf := bytes.NewBuffer(bodyJsonMarshal)

	req, err := http.NewRequest("POST", addRoleString, bodyBuf)
	if err != nil {
		return GenericMessage{}, err
	}
	req.Header.Add("Cookie", s.AuthCookie)
	resp, err := s.HttpClient.Do(req)
	if err != nil {
		return GenericMessage{}, err
	}
	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)

	if err != nil {
		return GenericMessage{}, err
	}

	genericMessage := GenericMessage{}
	err = json.Unmarshal(bodyBytes, &genericMessage)

	if err != nil {
		return GenericMessage{}, err
	}

	return genericMessage, nil
}

func (s *SynapseClient) DeleteRole(roleName string) (GenericMessage, error) {
	deleteRoleString := fmt.Sprintf("https://%s:%s%s", s.Host, s.Port, deleteRole)
	bodyJson := map[string]string{
		"name": roleName,
	}
	bodyJsonMarshal, _ := json.Marshal(bodyJson)

	bodyBuf := bytes.NewBuffer(bodyJsonMarshal)

	req, err := http.NewRequest("POST", deleteRoleString, bodyBuf)
	if err != nil {
		return GenericMessage{}, err
	}
	req.Header.Add("Cookie", s.AuthCookie)
	resp, err := s.HttpClient.Do(req)
	if err != nil {
		return GenericMessage{}, err
	}
	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)

	if err != nil {
		return GenericMessage{}, err
	}

	genericMessage := GenericMessage{}
	err = json.Unmarshal(bodyBytes, &genericMessage)

	if err != nil {
		return GenericMessage{}, err
	}

	return genericMessage, nil
}

func (s *SynapseClient) ModifyUser(iden string, user UserMod) (GenericMessage, error) {
	modUserString := fmt.Sprintf("https://%s:%s%s%s", s.Host, s.Port, modUser, iden)
	bodyJsonMarshal, _ := json.Marshal(user)
	bodyBuf := bytes.NewBuffer(bodyJsonMarshal)

	req, err := http.NewRequest("POST", modUserString, bodyBuf)
	if err != nil {
		return GenericMessage{}, err
	}
	req.Header.Add("Cookie", s.AuthCookie)
	resp, err := s.HttpClient.Do(req)
	if err != nil {
		return GenericMessage{}, err
	}
	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)

	if err != nil {
		return GenericMessage{}, err
	}
	fmt.Println(string(bodyBytes))
	genericMessage := GenericMessage{}
	err = json.Unmarshal(bodyBytes, &genericMessage)

	return genericMessage, nil
}

func (s *SynapseClient) ChangePassword(iden string, password string) (GenericMessage, error) {
	changePassString := fmt.Sprintf("https://%s:%s%s%s", s.Host, s.Port, changePass, iden)
	bodyJson := map[string]string{
		"passwd": password,
	}
	bodyJsonMarshal, _ := json.Marshal(bodyJson)

	bodyBuf := bytes.NewBuffer(bodyJsonMarshal)

	req, err := http.NewRequest("POST", changePassString, bodyBuf)
	if err != nil {
		return GenericMessage{}, err
	}
	req.Header.Add("Cookie", s.AuthCookie)
	resp, err := s.HttpClient.Do(req)
	if err != nil {
		return GenericMessage{}, err
	}
	defer resp.Body.Close()
	bodyBytes, err := io.ReadAll(resp.Body)

	if err != nil {
		return GenericMessage{}, err
	}

	genericMessage := GenericMessage{}
	err = json.Unmarshal(bodyBytes, &genericMessage)

	return genericMessage, nil
}
