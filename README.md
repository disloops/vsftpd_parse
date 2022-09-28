# VSFTPD Log Parser

VSFTPD Log Parser is a tool for pulling authentication data from a VSFTPD log.

#### Information

This script accepts a VSFTPD log file as input. It pulls all username/password combinations from the file and exports them as text or CSV.

Note: The script is currently designed for a server that only allows anonymous connections. This VSFTPD configuration results in a specific log format since passwords are not accepted for non-anonymous usernames. The script could easily be modified to handle non-anonymous logins instead.

#### Disclaimer

THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#### Usage

```
usage: vsftpd_parse.py [-h] [-i INPUT] [-o {csv,txt}]

optional arguments:
  -h, --help            Show this message and exit
                        
  -i INPUT, --input INPUT
                        The log file name you want to parse
  -o {csv,txt}, --output {csv,txt}
                        The format of the results
```