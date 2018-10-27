# Remove all the stop words from a file
file_name = "as.txt"
b_file = open(file_name)

file_name = "words"
w_file = open(file_name)

words = []
for s in w_file:
  v = s.split()
  for i in v:
    words.append(i)

for s in b_file:
  v = s.split();
  for i in v:
    if (i not in chars):
      i = i.lower()
    if (i not in words):
      print(i)age: script.pl words text >newfile
      use English;

      # poor man's argument handler
      open(WORDS, shift @ARGV) || die "failed to open words file: $!";
      open(REPLACE, shift @ARGV) || die "failed to open replacement file: $!";

      my @words;
      # get all words into an array
      while ($_=<WORDS>) { 
        chop; # strip eol
          push @words, split; # break up words on line
          }

          # (optional)
          # sort by length (makes sure smaller words don't trump bigger ones); ie, "then" vs "the"
          @words=sort { length($b) <=> length($a) } @words;

          # slurp text file into one variable.
          undef $RS;
          $text = <REPLACE>;

          # now for each word, do a global search-and-replace; make sure only words are replaced; remove possible following space.
          foreach $word (@words) { 
               $text =~ s/\b\Q$word\E\s?//sg;
               }

               # output "fixed" text
               print $text;



