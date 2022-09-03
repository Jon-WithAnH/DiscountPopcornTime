import java.util.*; 
import java.io.*;
// https://coderbyte.com/sl-candidate?promo=eulerity-60unv:backend-develop-spm5m8o38d
class Main {

  public static String StringChallenge(String str) {
    String submit_str = "";

    // iterate through each unique occurance of a character
    for (int i = 0; i < str.length(); i++){
      char char_at_index_i = str.charAt(i);
      int j = 0; // outside of loop to help with the final set of chars

      // iterate through the list until we find a different character and repeat
      // NOTE: we could do optimations for how we parse through the list.
      // The lengths of the given string are small, so speed isn't much of a concern
      // Otherwise, we might considering using binary search or a skip list at least to increase preformance
      for (j = i; j < str.length();j++){
        if (str.charAt(j) != (char_at_index_i)){
          submit_str += String.valueOf(j-i) + char_at_index_i;
          i = j - 1;
          break;
        }
        
      }
      if (j == str.length()){
        // End of String, so we can just grab the character at i and calcuate how far out we've moved in the string
        submit_str += String.valueOf(j-i) + char_at_index_i;
        break;
      }

    }
    str = submit_str;
    return str;
  }

  public static void main (String[] args) {  
    // keep this function call here     
    // Scanner s = new Scanner(System.in);
    System.out.print(StringChallenge("aabbcdeeffffff")); 
  }

}