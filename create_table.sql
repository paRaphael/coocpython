CREATE TABLE words (
            word_id int,
            word varchar2(255),
            CONSTRAINT pk_id_words PRIMARY KEY(word_id));

CREATE TABLE coocurence (
            word1_id int,
            word2_id int,
            count int,
            window_size int,
            CONSTRAINT pk_id_coocurence PRIMARY KEY(word1_id, word2_id),
            CONSTRAINT fk_id_coocurence_1 FOREIGN KEY (word1_id) REFERENCES words(word_id) ON DELETE CASCADE,
            CONSTRAINT fk_id_coocurence_2 FOREIGN KEY (word2_id) REFERENCES words(word_id) ON DELETE CASCADE );
			
		CREATE INDEX idx_word1_
            ON coocurence (word1_id);
		
		CREATE INDEX idx_word2_
            ON coocurence (word2_id);
		
		CREATE INDEX idx_window_size
            ON coocurence (window_size);