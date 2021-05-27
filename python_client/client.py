import asyncio
import websockets
import json

Fs = 1000
#сигнал
sig = [-0.04736953792203903, -0.00022657902192498846, -0.0007384649878918087, -0.0016730078943926745, -0.0030521630233712924, -0.004852890086638329, -0.00703487778393396, -0.009548368840950448, -0.01232968369739948, -0.015305200652659954, -0.0184009892210025, -0.021546908202937098, -0.024680792169470934, -0.027749457413147948, -0.03070682071774621, -0.03351720804855521, -0.03615073318676528, -0.03857226198861546, -0.04074083310242274, -0.04262108047956247, -0.04419631724571363, -0.045462962659406525, -0.04641473984290947, -0.04704325269604282, -0.04735099867273705, -0.04736088905682384, -0.047117975502426745, -0.046690330719608146, -0.04616383384427412, -0.04562169450000237, -0.045124711139352826, -0.044707488894114404, -0.044383036631787276, -0.04414292068591064, -0.04395565841928239, -0.04377300900916751, -0.0435467732813287, -0.043248919730970045, -0.04288149809838701, -0.042469318740141884, -0.042041054892826016, -0.04161823016394577, -0.04121503067385567, -0.040837322566547214, -0.04048655724465477, -0.040165067992613455, -0.03987728145311077, -0.03962863051974716, -0.03942827333079142, -0.03930314505057179, -0.039289885171087766, -0.03939712546063226, -0.039595873701116745, -0.03984953682597256, -0.04013462057041078, -0.04043066936337778, -0.04070736292037573, -0.040935915152487394, -0.04110706791254707, -0.0412305794413212, -0.041323084963748355, -0.04139393109712229, -0.041439932718129784, -0.04145493005389409, -0.04144190030798095, -0.04141661510476657, -0.04139809229407688, -0.041399365734459986, -0.04143265351557406, -0.04151644570738259, -0.04166688890976238, -0.04188300923952179, -0.04214580465648061, -0.042423479282172626, -0.04268246053691376, -0.042904157516822916, -0.04307975936805467, -0.04319134443002407, -0.04321253006934953, -0.04312376595444066, -0.04291784660127221, -0.0425989068353822, -0.04218462760672762, -0.04169741516050151, -0.041150830790729565, -0.04054956191997425, -0.039894022970134856, -0.03918494526307303, -0.03843006976558819, -0.03764239112497397, -0.03683324909088827, -0.036013529044640315, -0.035201562613222305, -0.0344262650744594, -0.033719648417059746, -0.03311072093490642, -0.03262366249124268, -0.03227196116079497, -0.03205430766071281, -0.031954383489083645, -0.031941647810095605, -0.031980550826691045, -0.03204624217352777, -0.03212721636371519, -0.03221222795739992, -0.032284298649007094, -0.03233123152462923, -0.03235442453218747, -0.03236646169601977, -0.03238638642553362, -0.032434200994109784, -0.03252276665078147, -0.03265255755743446, -0.03281526064861122, -0.03300094016636725, -0.0331942269198362, -0.03336616261069597, -0.033484919865575995, -0.03352944588177219, -0.03348533096858567, -0.03334937806002625, -0.033142802383490225, -0.03290341998439171, -0.03266668465703517, -0.032457904074838326, -0.03230034525812567, -0.032227312200876, -0.03227429838439515, -0.032459633341039795, -0.032784465406607725, -0.03323963065078077, -0.0337997502108598, -0.034421997701710824, -0.03505239633403065, -0.03563049018894773, -0.03610096718144695, -0.03641812735427747, -0.03652971836440351, -0.03637240414426605, -0.03589451737746856, -0.035082616512250066, -0.033967031007588334, -0.032599353540038914, -0.031031324011972172, -0.029318370843865335, -0.027531603872455627, -0.025758861826676013, -0.024088000232830902, -0.022586597745539068, -0.021299410973552063, -0.020250018304077442, -0.019433522755327788, -0.01882085547494035, -0.01837273473272087, -0.018044138296350296, -0.017782622295884534, -0.01752491303639896, -0.01719789676491306, -0.016730339838376306, -0.016061252783432678, -0.015139493506928456, -0.013928567325072649, -0.012411096625921107, -0.010583224592840414, -0.00845003300176106, -0.006028382326411384, -0.0033534480993662754, -0.0004855521148069071, 0.0024928103636600325, 0.005500869801468855, 0.008489421179874035, 0.011445641603082982, 0.01437665938173241, 0.017303011860452498, 0.02025505197456496, 0.023250199564837558, 0.02627672942471727, 0.029302685509697467, 0.0322939967802131, 0.035234957487913124, 0.03813367565901587, 0.04100488700046559, 0.04386063612484997, 0.04671283503373108, 0.049566668855283866, 0.052409889008128555, 0.05520530891553099, 0.05788962148948012, 0.06039040954901732, 0.06264944024541597, 0.06462223363797254, 0.06625473469848729, 0.06747285022842264, 0.06819872360370978, 0.06836851976355396, 0.06794424762767122, 0.06692837302812593, 0.06536745275298676, 0.06333353975654107, 0.06090185632032783, 0.05814727905474227, 0.05515100433135239, 0.0519912922294772, 0.048717864126102975, 0.04533561004580527, 0.04181897807031164, 0.03814802608180245, 0.034326513407112555, 0.03037167078942124, 0.02630156972260518, 0.02212509926489522, 0.017838499340056272, 0.01343733706580286, 0.008924813467115596, 0.004306962645668279, -0.0003948449407551968, -0.0051137633039250565, -0.009744547247311625, -0.014188501893743656, -0.018385198864511287, -0.022317092302309015, -0.02599617058708885, -0.029442976767737324, -0.032668025060686966, -0.03566544653025771, -0.03841846210751922, -0.040902676250012225, -0.04309009937795194, -0.044960576796442046, -0.04650400088160064, -0.04771244515812964, -0.04858356821204152, -0.04913214265915509, -0.04939695073085197, -0.049436857846788466, -0.04931658273272763, -0.04909858499896012, -0.048843184552279297, -0.04860368460398478, -0.04841540633881977, -0.04829250821988128, -0.04823579244510987, -0.04823289615737478, -0.04825745361497302, -0.04828663703219259, -0.0483184895065742, -0.04836965585855715, -0.048460831804564584, -0.04860166585387356, -0.04878626743091127, -0.04900346367829417, -0.04925132665457122, -0.049542513374601936, -0.04990171634120219, -0.050358352357778434, -0.05092984049398748, -0.05161126086510184, -0.05238373890621927, -0.05322169578008116, -0.05409006197222045, -0.05494249754470544, -0.05571928458788782, -0.0563410416234578, -0.05670595363437232, -0.05670333321777901, -0.056245412946347134, -0.05529258730952462, -0.053862385804374434, -0.052034719382814815, -0.04994265673063107, -0.047730350961584476, -0.04548710418591458, -0.043199240795069996, -0.04074655280598767, -0.03792725720637037, -0.03448682300427298, -0.030133924420997098, -0.024549222576113906, -0.01740191872749631, -0.008359539513809827, 0.002935908639828054, 0.016900401590436345, 0.03396651117215507, 0.054461427815116766, 0.07852110063017917, 0.1061062304808175, 0.13707481456157647, 0.1712670051473333, 0.20854993361689275, 0.24878610215381075, 0.2917865344076255, 0.33729013695955107, 0.38495674367984106, 0.43437871448635546, 0.4850902267510867, 0.5365510944737191, 0.5881262487277933, 0.6390722285140332, 0.688516253684671, 0.7354599641894752, 0.7788237599178509, 0.8174832964668037, 0.8503136216891743, 0.8762604108222548, 0.8943851812449075, 0.9038734308950924, 0.9040570072822428, 0.8944815296884223, 0.8749773160819256, 0.8456761806347766, 0.8069895219521556, 0.7596003032597779, 0.704500232983781, 0.6430328692850024, 0.5768255691979854, 0.5076109933888748, 0.4370726605548062, 0.3667669245814561, 0.2980895730965942, 0.23224270355297327, 0.1701993852017672, 0.1127050112236048, 0.060303313120360795, 0.013352347381540399, -0.027970424725848604, -0.0636562061875731, -0.09384082829105861, -0.11877824947688724, -0.13881139781415894, -0.15434231480188315, -0.16580670903379244, -0.1736587001555628, -0.17836628148646533, -0.18040247538378626, -0.18022924324458733, -0.17827084874143154, -0.17488640352196438, -0.17037515529673966, -0.16499604631603826, -0.15896718215914593, -0.15246713679041732, -0.14565425726567963, -0.13868019826767547, -0.1316875026093519, -0.12480823762028717, -0.1181694160854481, -0.11189332708263043, -0.10608607450761887, -0.10082347378435709, -0.09615031221735244, -0.09209316843831755, -0.08867127919967131, -0.0858954203896272, -0.08375746548898587, -0.08222251719746657, -0.08122873596349289, -0.08069025782266968, -0.08050991402323202, -0.08060041689551524, -0.08089353746664923, -0.08133862065070041, -0.08189611863808036, -0.08252029499059817, -0.08315148182253232, -0.08372964572580711, -0.08421297068752238, -0.08458808254335076, -0.08485956706824112, -0.0850328367994521, -0.08511352378733063, -0.08511294464301898, -0.08504496223110908, -0.08491412618983889, -0.08470860332474911, -0.08440933648818719, -0.0840027874339352, -0.0834805866132014, -0.08283608893428644, -0.08207261196101331, -0.08121030661169779, -0.08028212543454293, -0.07932362715043736, -0.07835731946790012, -0.07738308373092273, -0.07638352278253291, -0.07533700538819586, -0.07423885355375064, -0.0731191450095702, -0.07203506707601788, -0.07104721887711041, -0.07019684364294806, -0.06949160583985668, -0.06891245659648663, -0.06843833115456331, -0.06806218890419807, -0.06778648830703206, -0.06760945084340425, -0.06751348467388808, -0.06746827694348821, -0.06744447127553152, -0.06741963605536916, -0.06737736887119375, -0.06730524939137283, -0.06719031509303973, -0.0670130898515935, -0.06674928437360886, -0.06638441062794384, -0.06592337181204606, -0.06538528153280233, -0.06479662427306522, -0.06419131912061408, -0.06361608018519431, -0.06312719748337865, -0.0627744295049562, -0.06258881759363745, -0.06257932102836485, -0.06273702029848248, -0.06304794824255126, -0.06349753864401976, -0.06405839514542976, -0.06468215491509866, -0.06530659648086135, -0.06586640022483199, -0.0662999117154347, -0.06655216264407779, -0.06657807277887533, -0.06635857697109064, -0.0659115590204563, -0.06526698618521826, -0.06444599220918318, -0.06347352718276637, -0.06239026557623809, -0.06125376525120389, -0.06012851312907565, -0.059067064595937815, -0.05810039999587609, -0.05723410143773243, -0.05645541019570189, -0.05575103371823504, -0.055111800097812115, -0.054524422247081906, -0.05396969058354264, -0.05343292731675826, -0.052906268201479, -0.05238159899942405, -0.05185641969345588, -0.05134113366105546, -0.050853207319784884, -0.050406730297247515, -0.050009488343278785, -0.049670145897289145, -0.04940071923567237, -0.04920794822297401, -0.0490828756371576, -0.04899756971404164, -0.04891416396295036, -0.04879836691112169, -0.04862401180119534, -0.04837054720898864, -0.048019927333372556, -0.04755028758426409, -0.04693074781425734, -0.04613274011411857, -0.04515087399340318, -0.04400950921110868, -0.04276014106058546, -0.04147364118826599, -0.040213285762294736, -0.03900382192101036, -0.03782524020063969, -0.0366277056947688, -0.03534852963759276, -0.03393796059836875, -0.03238833906316837, -0.030726956159728716, -0.028979991846284615, -0.027158873754513757, -0.02527950392863821, -0.023377519768084665, -0.021497933910600783, -0.019680706641852983, -0.01795739258608739, -0.016356828129388334, -0.014919697868706968, -0.01369936490072086, -0.012739501840596724, -0.01205484305068701, -0.011625401378152784, -0.011402841392448775, -0.01133213086841581, -0.011365345739599532, -0.011448523260956894, -0.011516220141756291, -0.011509519756583694, -0.011385428148974438, -0.011111432564704593, -0.010656614614311617, -0.009987993510385608, -0.00908016616749822, -0.007924033543005788, -0.006521281111866653, -0.0048734530092969216, -0.0029768080082038448, -0.000832730672621986, 0.0015317671580977286, 0.0040580432998986015, 0.006668018418487986, 0.009282391953638195, 0.011835470209615184, 0.014279052264776921, 0.016583210317172057, 0.018735971760532, 0.020733867283704494, 0.022573786717108715, 0.02425804046597512, 0.025800490676635562, 0.027225898611613304, 0.028571096119241773, 0.029881352628296422, 0.031202406553529693, 0.03257884485391263, 0.03404865247379471, 0.03563428373054378, 0.03734081657830719, 0.03915858989632709, 0.04106589832916409, 0.04303164370909989, 0.04502319383014592, 0.047018577477399834, 0.04901795616257536, 0.05103960875769464, 0.05309234675694667, 0.055160568652464013, 0.057217949505290626, 0.0592399822235576, 0.06121145938412855, 0.06314422122370876, 0.06508896829164601, 0.06711662824455242, 0.06928385044547991, 0.07160618614395928, 0.07405310803453713, 0.07657933624877811, 0.07916525238278306, 0.08182145486390162, 0.08455932455847474, 0.08735999481410552, 0.09016902284860726, 0.09291754333792832, 0.0955463196887817, 0.09801379501350747, 0.100289619112866, 0.10234796215121862, 0.10416458725143617, 0.105714295694086, 0.10698003562742749, 0.10797066464199385, 0.10871567550258997, 0.10923950864848421, 0.10955054387697423, 0.109650974702989, 0.10955401543743479, 0.10929505255835391, 0.1089295816617841, 0.10852205243478735, 0.10813080941602657, 0.10779300278583612, 0.10750925986223991, 0.10724229405986524, 0.10694791268368066, 0.10660765735598876, 0.10622563174713434, 0.10580429121793376, 0.105323714817163, 0.10473582221195554, 0.10398357958503139, 0.10303400413842813, 0.10189260470929022, 0.10058505934365818, 0.09913207508748773, 0.0975452888288811, 0.0958337808825673, 0.09400865232192386, 0.0920919262237548, 0.09012075221327263, 0.08813442912606548, 0.08615802282601678, 0.08420004618631728, 0.08225529918315015, 0.08030169762618314, 0.07829738660106036, 0.07618543441763936, 0.07391304561935595, 0.07145255352435372, 0.06880335676943415, 0.06598699893260161, 0.06304064328604778, 0.059999648271207046, 0.056886666181660175, 0.05371657937321253, 0.05049788090371765, 0.047225641676098565, 0.04388337895972409, 0.0404581208890987, 0.03695361322477868, 0.033384228820912194, 0.02975824985698549, 0.026085620717491587, 0.0223967623724464, 0.018722795081910413, 0.015059198731137346, 0.011374236521008427, 0.00764786289748002, 0.0038831421440236364, 9.205368614653374e-05, -0.003711288404051174, -0.007508390318400374, -0.011273406346279814, -0.014978170431180876, -0.018605428949735187, -0.022150322354771712, -0.0256065173393189, -0.028955599073279072, -0.03217299886851786, -0.03524559522278399, -0.03817851954915413, -0.04098634533795863, -0.043686415034950576, -0.04629340434052867, -0.048814465595414976, -0.051257527391904374, -0.053640474113324114, -0.05598376862970974, -0.05829919115218705, -0.06059258445695016, -0.06286959897548763, -0.06512540523455515, -0.06733112080884697, -0.06944139035301206, -0.07141559736920175, -0.07322413128405521, -0.07483862449524081, -0.07622888328645022, -0.07736994094397306, -0.07824794860071375, -0.07886487297916896, -0.07924676007800706, -0.07944437209653807, -0.07951654977296792, -0.07951087037303749, -0.07945188884945469, -0.07933420208368534, -0.07913005583086125, -0.07881791595753071, -0.07840427366758974, -0.0779103789063417, -0.0773408337009001, -0.07667237103507228, -0.07587686482641798, -0.07495063331941493, -0.07391607151690151, -0.07281111309430578, -0.07169748371278052, -0.07066765866423402, -0.06981599736000077, -0.06919868561730065, -0.06882991592509824, -0.0686987153745442, -0.06877370102013154, -0.06901300391794203, -0.06937962246635117, -0.06983888497023145, -0.07035676618104392, -0.07091073326174624, -0.07149254243219039, -0.07210229655359285, -0.07274033083262112, -0.07339865097840022, -0.07406147907625964, -0.0747114878622251, -0.07532953567046644, -0.07589113948981567, -0.07636685721722511, -0.07673366217922695, -0.07699261469043946, -0.07716663055039952, -0.077283370146483, -0.0773707451195301, -0.0774518779374194, -0.07752755200874006, -0.07757901319243084, -0.077594209142399, -0.07758376028828544, -0.07758232198549563, -0.07763434846908601, -0.07777401418090439, -0.07801829740362086, -0.07835953386267201, -0.07876171802861864, -0.07917515684951267, -0.07955767495494462, -0.07988250528529978, -0.08012167523462367, -0.08023835630467223, -0.08021134014179303, -0.08005705160593712, -0.0798253101165708, -0.07957707499704895, -0.07936697708618999, -0.07924200990549098, -0.07923605122636347, -0.07935774881514404, -0.0795948076369596, -0.07992884850336336, -0.08034607620550849, -0.08083851409560623, -0.08139094250949813, -0.0819735870290752, -0.08255584703392554, -0.08312188681981728, -0.08366818196656343, -0.08419108696793207, -0.0846830479382142, -0.08512907418945634, -0.08549888834449232, -0.08576210827984845, -0.08591605648794726, -0.08598202756317999, -0.08598170215016214, -0.08593084659094538, -0.08584647944822986, -0.08574274985527065, -0.08561514792255277, -0.08544137854991635, -0.0851973086439915, -0.0848551466286179, -0.08437662890330451, -0.08373224583670111, -0.08292244511084983, -0.08196980292015273, -0.08089745669553948, -0.0797212145177912, -0.07845689277284873, -0.07712824024755659, -0.07577122038439148, -0.07443429226296606, -0.07316874082090268, -0.07201209326539347, -0.07098378387576329, -0.07009788759896175, -0.06936736119622175, -0.06879391310869283, -0.0683628365140166, -0.06804460337736093, -0.06780229064083257, -0.06760738508251771, -0.06744264399018943, -0.06728930700580972, -0.06712855953493065, -0.06694561159399753, -0.06671814222778205, -0.06641126755223559, -0.06598920231720427, -0.06543598213080548, -0.06476396248575798, -0.06399786401674536, -0.0631594064281084, -0.06226566979959029, -0.061332280007004594, -0.06037618768670652, -0.05941326351677791, -0.05845246725483183, -0.057502245546286634, -0.05659565324861678, -0.05579836814855568, -0.05517704313507173, -0.05477057634153092, -0.0545935991279099, -0.05464489221478237, -0.05490399700150709, -0.05533896303146317, -0.055919018870429556, -0.05660739791624632, -0.05735812836098878, -0.058123486806858735, -0.058852976927968204, -0.059497215396375265, -0.06002326624880673, -0.060427419799489235, -0.06072992532170921, -0.060952725778678385, -0.06110747411186933, -0.0612049832606287, -0.06126527152529892, -0.06131258832271307, -0.06136035945725324, -0.06140135970492566, -0.061416371306283725, -0.061388627353276264, -0.06131015352979276, -0.06117798161375028, -0.06097646782435399, -0.060671852197875825, -0.0602280925904225, -0.05961513244895411, -0.058812649445513315, -0.057821686931913446, -0.05666967835356435, -0.05540575345452806, -0.05409719993239641, -0.05282148261514205, -0.051652039874820935, -0.05064476451272308, -0.04982581282947123, -0.04919006719495742, -0.04871371005408858, -0.04836642801120208, -0.04811678798757516, -0.047932619796921414, -0.04778090832472873, -0.04764157992641114, -0.04752170786394537, -0.047437059532571095, -0.04738578525056236, -0.04735619719514137, -0.047345183115303516, -0.04735323021429148, -0.04736953792203903]
d = 1
async def monitor1():
    #під'єднання
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        print('monitor 1 conected')
        while True:
            #Кожну секунду надсилаємо данні
            blog = {'DATA': sig, 'id': 1}
            #blog2 = {'DATA': sig, 'id': 2}
            to_json = json.dumps(blog)
            #to_json2 = json.dumps(blog2)
            await websocket.send(to_json)
            await asyncio.sleep(d)
            #відправляємо у веб сокет
            #await websocket.send(to_json2)
            await asyncio.sleep(d)
        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(monitor1())