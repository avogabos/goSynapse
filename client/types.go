package client

type Users struct {
	Status string `json:"status"`
	Result []struct {
		Type  string        `json:"type"`
		Iden  string        `json:"iden"`
		Name  string        `json:"name"`
		Rules []interface{} `json:"rules"`
		Roles []struct {
			Type      string                            `json:"type"`
			Iden      string                            `json:"iden"`
			Name      string                            `json:"name"`
			Rules     []interface{}                     `json:"rules"`
			Authgates map[string]map[string]interface{} `json:"authgates"`
		} `json:"roles"`
		Admin     bool                              `json:"admin"`
		Email     string                            `json:"email"`
		Locked    bool                              `json:"locked"`
		Archived  bool                              `json:"archived"`
		Authgates map[string]map[string]interface{} `json:"authgates"`
	} `json:"result"`
}

type Nodes map[string]string

type Feed struct {
	Items Nodes  `json:"items"`
	View  string `json:"view"`
}

type Storm struct {
	Query  string   `json:"query"`
	Opts   []string ` json:"opts,omitempty"`
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
		Type      string                     `json:"type"`
		Iden      string                     `json:"iden"`
		Name      string                     `json:"name"`
		Rules     []interface{}              `json:"rules"`
		Authgates map[string][][]interface{} `json:"authgates"`
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
