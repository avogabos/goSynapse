package client

type Users struct {
	Status string `json:"status"`
	Result []struct {
		Type  string        `json:"type"`
		Iden  string        `json:"iden"`
		Name  string        `json:"name"`
		Rules []interface{} `json:"rules"`
		Roles []struct {
			Type      string        `json:"type"`
			Iden      string        `json:"iden"`
			Name      string        `json:"name"`
			Rules     []interface{} `json:"rules"`
			Authgates struct {
				Fbc01A0C8170508Af6A9A759046Cdb struct {
					Rules [][]interface{} `json:"rules"`
				} `json:"03fbc01a0c8170508af6a9a759046cdb"`
				B599864235Fd98225D8Db5Bdc6D632E4 struct {
					Rules [][]interface{} `json:"rules"`
				} `json:"b599864235fd98225d8db5bdc6d632e4"`
			} `json:"authgates"`
		} `json:"roles"`
		Admin     bool        `json:"admin"`
		Email     interface{} `json:"email"`
		Locked    bool        `json:"locked"`
		Archived  bool        `json:"archived"`
		Authgates struct {
			Fbc01A0C8170508Af6A9A759046Cdb struct {
				Admin bool `json:"admin"`
			} `json:"03fbc01a0c8170508af6a9a759046cdb,omitempty"`
			B599864235Fd98225D8Db5Bdc6D632E4 struct {
				Admin bool `json:"admin"`
			} `json:"b599864235fd98225d8db5bdc6d632e4,omitempty"`
		} `json:"authgates"`
	} `json:"result"`
}

type Nodes map[string]string

type Feed struct {
	Items Nodes  `json:"items"`
	View  string `json:"view"`
}

type Storm struct {
	Query  string   `json:"query"`
	Opts   []string `json:"opts"`
	Stream string   `json:"stream"`
}

type StormCall struct {
	Query string   `json:"query"`
	Opts  []string `json:"opts"`
}

type UserMod map[string]interface{}

func (u UserMod) SetAdmin(admin bool) {
	u["admin"] = admin
}

func (u UserMod) SetEmail(email string) {
	u["email"] = email
}

func (u UserMod) SetLocked(locked bool) {
	u["locked"] = locked
}

func (u UserMod) SetArchived(archived bool) {
	u["archived"] = archived
}

func (u UserMod) SetName(name string) {
	u["name"] = name
}

func (u UserMod) SetRoles(roles []string) {
	u["roles"] = roles
}

type ErrorMessage struct {
	Status string `json:"status"`
	Code   string `json:"code"`
	Mesg   string `json:"mesg"`
}

type Roles struct {
	Status string `json:"status"`
	Result []struct {
		Type      string        `json:"type"`
		Iden      string        `json:"iden"`
		Name      string        `json:"name"`
		Rules     []interface{} `json:"rules"`
		Authgates struct {
			Fbc01A0C8170508Af6A9A759046Cdb struct {
				Rules [][]interface{} `json:"rules"`
			} `json:"03fbc01a0c8170508af6a9a759046cdb"`
			B599864235Fd98225D8Db5Bdc6D632E4 struct {
				Rules [][]interface{} `json:"rules"`
			} `json:"b599864235fd98225d8db5bdc6d632e4"`
		} `json:"authgates"`
	} `json:"result"`
}

type Active struct {
	Status string `json:"status"`
	Result struct {
		Active bool `json:"active"`
	} `json:"result"`
}

type GenericMessage struct {
	Status string   `json:"status"`
	Result struct{} `json:"result"`
}

type CortexModel struct {
	Types struct {
	} `json:"types"`
	Forms struct {
	} `json:"forms"`
	Tagprops struct {
	} `json:"tagprops"`
}

type AxonDelete struct {
	Status string          `json:"status"`
	Result map[string]bool `json:"result"`
}
