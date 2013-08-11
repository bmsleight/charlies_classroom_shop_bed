#!/bin/bash
#

echo $1 $2 $3 $4

cat > $1 <<'_EOF'
<svg xmlns="http://www.w3.org/2000/svg"
      width="1615px" height="765px" version="1.1">
_EOF
echo "      <text x=\"1000\" y=\"560\" font-family=\"sans-serif\" font-size=\"40px\" fill=\"white\">$2</text>">>$1
echo "      <text x=\"1000\" y=\"620\" font-family=\"sans-serif\" font-size=\"40px\" fill=\"white\">$3</text>">>$1
echo "      <text x=\"1000\" y=\"680\" font-family=\"sans-serif\" font-size=\"40px\" fill=\"white\">$4</text>">>$1
echo "</svg>">>$1

