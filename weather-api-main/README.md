# APIproject

## launch servers

> cd APIproject

**Django server**

> python manage.py runserver

**Meilisearch server**

> meilisearch-windows-amd64.exe

## API routes

### Geography API

#### Département

**Methode :** _GET_

**Token requiered :** _access_

**Url :**

> 127.0.0.1:8000/geography/departements/all/

**Parameters :** None

**Return :** Departements map data.

#### Communes

**Methode :** _POST_

**Token requiered :** _access_

**Url :**

> 127.0.0.1:8000/geography/departements/communes/all

**Parameters :**

- _dep_ : departement's number and name. (Example : '01-ain')

**Return :** Towns map data.

#### Search communes

**Methode :** _POST_

**Token requiered :** _access_

**Url :**

> 127.0.0.1:8000/geography/search/communes

**Parameters :**

- _query_ : Part of commune's number or name or both to search in the database.

**Return :** List of corresponding towns.

### User management API

#### Register

**Methode :** _POST_

**Token requiered :** _None_

**Url :**

> 127.0.0.1:8000/accounts/register

**Parameters :**

- _email_ : User's email.
- _password_ : User's password.

**Return :**

- _email_ : User's email.

#### Login

**Methode :** _POST_

**Token requiered :** _None_

**Url :**

> 127.0.0.1:8000/accounts/login

**Parameters :**

- _email_ : User's email.
- _password_ : User's password.

**Return :**

- _msg_ : success or error message.
- _refresh_ : refresh token.
- _access_ : access token.

#### Logout

**Methode :** _POST_

**Token requiered :** _access_

**Url :**

> 127.0.0.1:8000/accounts/logout

**Parameters :** _None_

**Return :**

- _msg_ : success or error message.

#### Change password

**Methode :** _POST_

**Token requiered :** _access_

**Url :**

> 127.0.0.1:8000/accounts/change-password

**Parameters :**

- _current_password_ : Current password.
- _new_password_ : New password.

**Return :** _None_ or _error message_

#### Refresh token

**Methode :** _POST_

**Token requiered :** _refresh_

**Url :**

> 127.0.0.1:8000/accounts/token-refresh/

**Parameters :**

- _refresh_ : refresh token.

**Return :**

- _access_ : access token.

#### Check token

**Methode :** _POST_

**Token requiered :** _None_

**Url :**

> 127.0.0.1:8000/accounts/token-check/

**Parameters :**

- *access_token* : access token of the user.

**Return :**

- _token_valid_ : 1 if token valid, 0 if not.

### Models

#### Predictions

**Methode :** _POST_

**Token requiered :** _access_

**Url :**

> 127.0.0.1:8000/models/prediction

**Parameters :**

- _postal_code_ : postal code of PV site.
- _latitude_ : latitude of PV site.
- _longitude_ : longitude of PV site.
- *nb_days* : number of days of prediction.

**Return :**

- _data_ : weather data with forecasts in json format.
