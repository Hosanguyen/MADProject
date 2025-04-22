USE mad;

-- User Table
CREATE TABLE user
  (
     id         CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     username   VARCHAR(255) NOT NULL UNIQUE,
     password   VARCHAR(255) NOT NULL,
     fullname   VARCHAR(255) NOT NULL,
     image_url  VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	   updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     role       VARCHAR(255) NOT NULL DEFAULT 'user'
  );

-- Pet Table
CREATE TABLE pet
  (
     id         CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     name       VARCHAR(255) NOT NULL,
     breed_name VARCHAR(255) NOT NULL,
     gender     VARCHAR(255) NOT NULL,
     birth_date DATE NULL,
     color      VARCHAR(255) NULL,
     height     FLOAT NOT NULL,
     weight     FLOAT NOT NULL,
     image_url  VARCHAR(255) NULL,
     note       VARCHAR(255) NULL,
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	   updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     userid     CHAR(36),
     FOREIGN KEY (userid) REFERENCES user(id) ON DELETE CASCADE
  );

-- Reminder Table
CREATE TABLE reminder
  (
     id            CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     type          VARCHAR(255),
     time_reminder TIMESTAMP,
     repeat_time   VARCHAR(255),
     note          VARCHAR(255),
     status        VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  );

-- Pet_Reminder Table
CREATE TABLE pet_reminder
  (
     id         CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     reminderid CHAR(36),
     petid      CHAR(36),
     FOREIGN KEY (petid) REFERENCES pet(id) ON DELETE CASCADE,
     FOREIGN KEY (reminderid) REFERENCES reminder(id) ON DELETE CASCADE
  );

-- Vaccination Table
CREATE TABLE vaccination
  (
     id            CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     type          VARCHAR(255),
     date          DATE,
     next_due_date DATE,
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     petid         CHAR(36),
     FOREIGN KEY (petid) REFERENCES pet(id) ON DELETE CASCADE
  );

-- Veterinarian Table
CREATE TABLE veterinarian
  (
     id             CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     name           VARCHAR(255),
     specialization VARCHAR(255),
     phone          VARCHAR(20),
     email          VARCHAR(50),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  );

-- Medical Report Table
CREATE TABLE medical_report
  (
     id           CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     title        VARCHAR(255),
     hospital     VARCHAR(255),
     veterinarian VARCHAR(255),
     description  VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     petid        CHAR(36),
     FOREIGN KEY (petid) REFERENCES pet(id) ON DELETE CASCADE
  );

-- Image Medical Report Table
CREATE TABLE image_medical_report
  (
     id               CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     image_url        VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     medical_reportid CHAR(36),
     FOREIGN KEY (medical_reportid) REFERENCES medical_report(id) ON DELETE CASCADE
  );

-- Post Table
CREATE TABLE post
  (
     id         CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     content    VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     userid     CHAR(36),
     FOREIGN KEY (userid) REFERENCES user(id) ON DELETE CASCADE
  );

-- Post Image Table
CREATE TABLE post_image
  (
     id         CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     image_url  VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     postid     CHAR(36),
     FOREIGN KEY (postid) REFERENCES post(id) ON DELETE CASCADE
  );

-- Comment Table
CREATE TABLE comment
  (
     id        CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     content   VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     userid    CHAR(36),
     postid    CHAR(36),
     FOREIGN KEY (userid) REFERENCES user(id) ON DELETE CASCADE,
     FOREIGN KEY (postid) REFERENCES post(id) ON DELETE CASCADE
  );

-- Reaction Table
CREATE TABLE reaction
  (
     id     CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     type   VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     postid CHAR(36),
     userid CHAR(36),
     FOREIGN KEY (postid) REFERENCES post(id) ON DELETE CASCADE,
     FOREIGN KEY (userid) REFERENCES user(id) ON DELETE CASCADE
  );

-- Nutrition Table  
CREATE TABLE nutrition
  (
     id              CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     name            VARCHAR(255),
     description     VARCHAR(255),
     recommended_for VARCHAR(255),
     nutrients       VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  );

-- Disease Table
CREATE TABLE disease
  (
     id         CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     name       VARCHAR(255),
     symptoms   VARCHAR(255),
     treatment  VARCHAR(255),
     prevention VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  );

-- Item Type Table
CREATE TABLE item_type
  (
     id   CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     name VARCHAR(255),
     unit VARCHAR(255),
     note VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  );

-- Item Table
CREATE TABLE item
  (
     id          CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     name        VARCHAR(255),
     price       FLOAT,
     quantity    INT,
     description VARCHAR(255),
     item_typeid CHAR(36),
     manufacturer VARCHAR(255),
     image_url VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     FOREIGN KEY (item_typeid) REFERENCES item_type(id) ON DELETE CASCADE
  );

-- Cart Table
CREATE TABLE cart
  (
     id         CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     userid     CHAR(36),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     FOREIGN KEY (userid) REFERENCES user(id) ON DELETE CASCADE
  );

-- Cart Item Table
CREATE TABLE cart_item
  (
     id         CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     quantity   INT,
     cartid     CHAR(36),
     itemid     CHAR(36),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     FOREIGN KEY (cartid) REFERENCES cart(id) ON DELETE CASCADE,
     FOREIGN KEY (itemid) REFERENCES item(id) ON DELETE CASCADE
  );

-- Order Table
CREATE TABLE `order`
  (
     id         CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     userid     CHAR(36),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     FOREIGN KEY (userid) REFERENCES user(id) ON DELETE CASCADE
  );

-- Order Item Table
CREATE TABLE order_item
  (
     id          CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     quantity    INT,
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     orderid     CHAR(36),
     cart_itemid CHAR(36),
     FOREIGN KEY (orderid) REFERENCES `order`(id) ON DELETE CASCADE,
     FOREIGN KEY (cart_itemid) REFERENCES cart_item(id) ON DELETE CASCADE
  );

-- GPS Device Table
CREATE TABLE gps_device
  (
     id         CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     name       VARCHAR(255),
     status     VARCHAR(255),
     battery    VARCHAR(10),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     petid      CHAR(36),
     FOREIGN KEY (petid) REFERENCES pet(id) ON DELETE CASCADE
  );

-- Diary Note Table
CREATE TABLE diary_note
  (
     id         CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     title      VARCHAR(255),
     start_time TIMESTAMP,-- why timestamp
     end_time   TIMESTAMP,-- why timestamp
     note       VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     petid      CHAR(36),
     FOREIGN KEY (petid) REFERENCES pet(id) ON DELETE CASCADE
  );

-- Static Type Table
CREATE TABLE statistic_type
  (
     id          CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     name        VARCHAR(255),
     unit        VARCHAR(255),
     description VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  );

-- Pet Statistic 
CREATE TABLE pet_statistic
  (
     id               CHAR(36) PRIMARY KEY DEFAULT (UUID()),
     value            FLOAT,
     recorded_at      DATETIME,
     note             VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     petid            CHAR(36),
     statistic_typeid CHAR(36),
     FOREIGN KEY (petid) REFERENCES pet(id) ON DELETE CASCADE,
     FOREIGN KEY (statistic_typeid) REFERENCES statistic_type(id) ON DELETE CASCADE
  ); 