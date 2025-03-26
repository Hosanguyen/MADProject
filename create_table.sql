USE mad;

-- User Table
CREATE TABLE user
  (
     id         INT PRIMARY KEY auto_increment,
     username   VARCHAR(255) NOT NULL,
     password   VARCHAR(255) NOT NULL,
     fullname   VARCHAR(255) NOT NULL,
     image_url  VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	 updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     role       VARCHAR(255) NOT NULL
  );

-- Pet Table
CREATE TABLE pet
  (
     id         INT PRIMARY KEY auto_increment,
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
     userid     INT,
     FOREIGN KEY (userid) REFERENCES user(id)
  );

-- Reminder Table
CREATE TABLE reminder
  (
     id            INT PRIMARY KEY auto_increment,
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
     id         INT PRIMARY KEY auto_increment,
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     reminderid INT,
     petid      INT,
     FOREIGN KEY (petid) REFERENCES pet(id),
     FOREIGN KEY (reminderid) REFERENCES reminder(id)
  );

-- Vaccination Table
CREATE TABLE vaccination
  (
     id            INT PRIMARY KEY auto_increment,
     type          VARCHAR(255),
     date          DATE,
     next_due_date DATE,
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     petid         INT,
     FOREIGN KEY (petid) REFERENCES pet(id)
  );

-- Veterinarian Table
CREATE TABLE veterinarian
  (
     id             INT PRIMARY KEY auto_increment,
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
     id           INT PRIMARY KEY auto_increment,
     title        VARCHAR(255),
     hospital     VARCHAR(255),
     veterinarian VARCHAR(255),
     description  VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     petid        INT,
     FOREIGN KEY (petid) REFERENCES pet(id)
  );

-- Image Medical Report Table
CREATE TABLE image_medical_report
  (
     id               INT PRIMARY KEY auto_increment,
     image_url        VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     medical_reportid INT,
     FOREIGN KEY (medical_reportid) REFERENCES medical_report(id)
  );

-- Post Table
CREATE TABLE post
  (
     id         INT PRIMARY KEY auto_increment,
     content    VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     userid     INT,
     FOREIGN KEY (userid) REFERENCES user(id)
  );

-- Post Image Table
CREATE TABLE post_image
  (
     id         INT PRIMARY KEY auto_increment,
     image_url  VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     postid     INT,
     FOREIGN KEY (postid) REFERENCES post(id)
  );

-- Comment Table
CREATE TABLE comment
  (
     id        INT PRIMARY KEY auto_increment,
     content   VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     userid    INT,
     postid    INT,
     FOREIGN KEY (userid) REFERENCES user(id),
     FOREIGN KEY (postid) REFERENCES post(id)
  );

-- Reaction Table
CREATE TABLE reaction
  (
     id     INT PRIMARY KEY auto_increment,
     type   VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     postid INT,
     userid INT,
     FOREIGN KEY (postid) REFERENCES post(id),
     FOREIGN KEY (userid) REFERENCES user(id)
  );

-- Nutrition Table  
CREATE TABLE nutrition
  (
     id              INT PRIMARY KEY auto_increment,
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
     id         INT PRIMARY KEY auto_increment,
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
     id   INT PRIMARY KEY auto_increment,
     name VARCHAR(255),
     unit VARCHAR(255),
     note VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  );

-- Item Table
CREATE TABLE item
  (
     id          INT PRIMARY KEY auto_increment,
     name        VARCHAR(255),
     price       FLOAT,
     quantity    INT,
     description VARCHAR(255),
     item_typeid INT,
     manufacturer VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     FOREIGN KEY (item_typeid) REFERENCES item_type(id)
  );

-- Cart Table
CREATE TABLE cart
  (
     id         INT PRIMARY KEY auto_increment,
     userid     INT,
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     FOREIGN KEY (userid) REFERENCES user(id)
  );

-- Cart Item Table
CREATE TABLE cart_item
  (
     id         INT PRIMARY KEY auto_increment,
     quantity   INT,
     cartid     INT,
     itemid     INT,
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     FOREIGN KEY (cartid) REFERENCES cart(id),
     FOREIGN KEY (itemid) REFERENCES item(id)
  );

-- Order Table
CREATE TABLE `order`
  (
     id         INT PRIMARY KEY auto_increment,
     userid     INT,
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     FOREIGN KEY (userid) REFERENCES user(id)
  );

-- Order Item Table
CREATE TABLE order_item
  (
     id          INT PRIMARY KEY auto_increment,
     quantity    INT,
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     orderid     INT,
     cart_itemid INT,
     FOREIGN KEY (orderid) REFERENCES `order`(id),
     FOREIGN KEY (cart_itemid) REFERENCES cart_item(id)
  );

-- GPS Device Table
CREATE TABLE gps_device
  (
     id         INT PRIMARY KEY auto_increment,
     name       VARCHAR(255),
     status     VARCHAR(255),
     battery    VARCHAR(10),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     petid      INT,
     FOREIGN KEY (petid) REFERENCES pet(id)
  );

-- Diary Note Table
CREATE TABLE diary_note
  (
     id         INT PRIMARY KEY auto_increment,
     title      VARCHAR(255),
     start_time TIMESTAMP,-- why timestamp
     end_time   TIMESTAMP,-- why timestamp
     note       VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     petid      INT,
     FOREIGN KEY (petid) REFERENCES pet(id)
  );

-- Static Type Table
CREATE TABLE statistic_type
  (
     id          INT PRIMARY KEY auto_increment,
     name        VARCHAR(255),
     unit        VARCHAR(255),
     description VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  );

-- Pet Statistic 
CREATE TABLE pet_statistic
  (
     id               INT PRIMARY KEY auto_increment,
     value            FLOAT,
     recorded_at      DATETIME,
     note             VARCHAR(255),
     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
     petid            INT,
     statistic_typeid INT,
     FOREIGN KEY (petid) REFERENCES pet(id),
     FOREIGN KEY (statistic_typeid) REFERENCES statistic_type(id)
  ); 