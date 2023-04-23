<template>
  <v-row justify="center" align="center">
    <v-col cols="12" class="d-flex justify-center">
      <v-card max-width="600px" elevation="0">
        <v-card-title class="headline">
          Análise de Risco
        </v-card-title>
        <v-card-text class="pb-0">
          <div id="map" style="width: 100%; height: 400px; z-index: 1;"></div>
          Clique no mapa e selecione o tipo de ocorrência a ser analisado:<br>
          <div>
            <v-autocomplete v-model="selected_occurence_type" label="Tipo de ocorrência" :items="occurence_type"/>
            <v-autocomplete v-model="selected_distrito" readonly label="Distrito" :items="location_distrito"/>
            <v-autocomplete v-model="selected_concelho" readonly label="Tipo de ocorrência" :items="location_concelho"/>
          </div>
          <v-divider class="mt-2"/>
        </v-card-text>
        <v-card-actions class="ma-2 d-block">
          <v-row style="width: 100%">
            <v-col cols="12" class="d-flex">
              <b v-if="awaitingState===1">PLEASE WAIT (up to 2min)...</b>
              <b v-if="awaitingState===2">RESULT:</b>
              <v-spacer />
              <v-btn @click="getHh" :disabled="!isReady || awaitingState > 0" color="primary" class="text-capitalize" elevation="6">
                Fazer análise!
              </v-btn>
            </v-col>
          </v-row>
          <v-row style="width: 100%" v-if="awaitingState===2">
            <v-col cols="12" class="pt-0">
              <small style="width: 100%;">Maior risco na região: {{ greatestRisk }}</small>
            </v-col>
            <v-col cols="12" class="pt-0">
              <small style="width: 100%;">Serão necessárias {{ hora_homem }} horas-homem para resolver o problema.</small>
            </v-col>
          </v-row>
          <v-row style="width: 100%" v-if="awaitingState===2">
            <v-col cols="12" class="text-center pt-0">
              <v-btn @click="tryAgain" dark color="red" class="text-lowercase" rounded depressed>Tentar novamente?</v-btn>
            </v-col>
          </v-row>
        </v-card-actions>
      </v-card>
    </v-col>
<!--    <v-col class="d-flex justify-center">-->
<!--      <v-card max-width="600px" elevation="0">-->
<!--        <v-card-title>Parameters</v-card-title>-->
<!--        <v-card-text>-->
<!--          Below you can find the meaning of each parameter<br>-->
<!--          <ul>-->
<!--            <li v-for="parameter in Object.keys(parameters)" :key="parameter">-->
<!--              <b>{{ parameter }}</b> [{{ parameters[parameter].type }}]: {{ parameters[parameter].desc }}-->
<!--            </li>-->
<!--          </ul>-->
<!--        </v-card-text>-->
<!--      </v-card>-->
<!--    </v-col>-->
  </v-row>
</template>

<script>
import 'leaflet/dist/leaflet.css';
import * as L from 'leaflet';
export default {
  name: 'IndexPage',
  computed: {
    isReady() {
      return this.selected_occurence_type && this.selected_distrito && this.selected_concelho;
    }
  },
  data() {return {
    selected_occurence_type: null,
    selected_distrito: null,
    selected_concelho: null,
    hora_homem: 0,
    greatestRisk: '',

    awaitingState: 0, // 0 - not begun, 1 - waiting, 2 - done

    occurence_type: ['Assistência e Prevenção a actividades humanas', 'Assistência em Saúde',
      'Incêndios Rurais', 'Incêndios Urbanos ou em Área Urbanizável', 'Acidentes',
      'Comprometimento total ou parcial de segurança, serviços ou estruturas',
      'Incêndios em Transportes', 'Intervenção em conflitos legais',
      'Acidentes industriais e tecnológicos',
      'Incêndios em Equipamento e Produtos', 'Incêndios em Detritos',
      'Fenómenos Naturais', 'Operações'],

    location_distrito:['PORTO', 'LISBOA', 'BRAGA', 'SETÚBAL', 'AVEIRO', 'SANTARÉM', 'VISEU', 'LEIRIA', 'FARO', 'COIMBRA', 'BRAGANÇA', 'VILA REAL', 'VIANA DO CASTELO', 'GUARDA', 'CASTELO BRANCO', 'PORTALEGRE', 'BEJA', 'ÉVORA'],

    location_concelho:['MOITA','CASTRO VERDE', 'MAFRA', 'RESENDE', 'SANTARÉM', 'GONDOMAR', 'MEALHADA',
    'CASTELO BRANCO', 'VILA NOVA DA BARQUINHA', 'VILA VELHA DE RÓDÃO', 'SABUGAL',
    'TONDELA', 'ALENQUER', 'SINTRA', 'PAREDES', 'OLIVEIRA DE AZEMÉIS', 'OEIRAS',
    'TOMAR', 'VILA NOVA DE FAMALICÃO', 'CASTRO DAIRE', 'TÁBUA', 'VILA DO CONDE',
    'SANTO TIRSO', 'VILA FLOR', 'LEIRIA', 'PONTE DE LIMA', 'PAÇOS DE FERREIRA',
    'CALDAS DA RAINHA', 'BARCELOS', 'PORTIMÃO', 'LAGOS', 'FORNOS DE ALGODRES',
    'VAGOS', 'VALE DE CAMBRA', 'ALBERGARIA-A-VELHA', 'SÃO JOÃO DA MADEIRA',
    'TAVIRA', 'GOLEGÃ', 'RIO MAIOR', 'ABRANTES', 'MAÇÃO', 'ALMEIDA',
    'OLIVEIRA DO HOSPITAL', 'POMBAL', 'VALPAÇOS', 'LAMEGO', 'PENALVA DO CASTELO',
    'GUARDA', 'ALCANENA', 'PENAMACOR', 'FERREIRA DO ZÊZERE', 'COVILHÃ', 'OURÉM',
    'SÁTÃO', 'VILA NOVA DE PAIVA', 'VISEU', 'SILVES', 'CARTAXO', 'ALPIARÇA',
    'VILA NOVA DE GAIA', 'MONCHIQUE', 'ODEMIRA', 'SARDOAL', 'LOUSADA', 'VALONGO',
    'ALJEZUR', 'TORRES VEDRAS', 'OLEIROS', 'MAIA', 'PORTO DE MÓS', 'ALMEIRIM',
    'AVEIRO', 'FARO', 'VILA REAL DE SANTO ANTÓNIO', 'CASCAIS', 'TORRES NOVAS',
    'OLHÃO', 'BENAVENTE', 'BEJA', 'CASTRO MARIM', 'SOURE', 'VILA DO BISPO',
    'VOUZELA', 'ENTRONCAMENTO', 'LAGOA', 'FUNDÃO', 'SEIA', 'NELAS', 'BOMBARRAL',
    'CHAMUSCA', 'SALVATERRA DE MAGOS', 'ARGANIL', 'SESIMBRA', 'ALCÁCER DO SAL',
    'IDANHA-A-NOVA', 'CAMINHA', 'AROUCA', 'VALENÇA', 'AMARANTE', 'PENAFIEL',
    'PINHEL', 'COIMBRA', 'PENACOVA', 'CONDEIXA-A-NOVA', 'BORBA', 'CARREGAL DO SAL',
    'LOURES', 'REGUENGOS DE MONSARAZ', 'PALMELA', 'OLIVEIRA DO BAIRRO',
    'LOURINHÃ', 'ALBUFEIRA', 'LOULÉ', 'MELGAÇO', 'SEIXAL', 'MANTEIGAS', 'AMADORA',
    'CINFÃES', 'MARCO DE CANAVESES', 'MONÇÃO', 'MARINHA GRANDE', 'FELGUEIRAS',
    'FIGUEIRA DA FOZ', 'SÃO BRÁS DE ALPORTEL', 'CADAVAL', 'ARMAMAR',
    'ARCOS DE VALDEVEZ', 'SÃO PEDRO DO SUL', 'MOURÃO', 'PORTO',
    'PAREDES DE COURA', 'MÊDA', 'PEDRÓGÃO GRANDE', 'CONSTÂNCIA', 'VENDAS NOVAS',
    'ÉVORA', 'ODIVELAS', 'PENICHE', 'SERTÃ', 'PENEDONO', 'CELORICO DA BEIRA',
    'VILA FRANCA DE XIRA', 'ALFÂNDEGA DA FÉ', 'TORRE DE MONCORVO', 'ANADIA',
    'MACEDO DE CAVALEIROS', 'PORTALEGRE', 'TABUAÇO', 'ESTREMOZ', 'ALCOCHETE',
    'ALVAIÁZERE', 'ÁGUEDA', 'BRAGANÇA', 'PONTE DA BARCA', 'BARREIRO', 'ALMADA',
    'PÓVOA DE LANHOSO', 'VILA POUCA DE AGUIAR', 'SANTA MARIA DA FEIRA', 'BRAGA',
    'SETÚBAL', 'LISBOA', 'MIRANDA DO CORVO', 'ÍLHAVO', 'CUBA',
    'FIGUEIRA DE CASTELO RODRIGO', 'ELVAS', 'FAFE', 'GUIMARÃES', 'MATOSINHOS',
    'ANSIÃO', 'MONTALEGRE', 'SOUSEL', 'PENELA', 'SANTIAGO DO CACÉM', 'AMARES',
    'MOIMENTA DA BEIRA', 'CANTANHEDE', 'CHAVES', 'CABECEIRAS DE BASTO',
    'VILA NOVA DE POIARES', 'BELMONTE', 'TROFA', 'SINES', 'CORUCHE',
    'SÃO JOÃO DA PESQUEIRA', 'CASTELO DE VIDE', 'VILA VERDE', 'MONTEMOR-O-NOVO',
    'FREIXO DE ESPADA À CINTA', 'NISA', 'LOUSÃ', 'VILA REAL', 'PÓVOA DE VARZIM',
    'ALCOBAÇA', 'ESTARREJA', 'VIEIRA DO MINHO', 'SEVER DO VOUGA', 'OVAR',
    'GOUVEIA', 'ALVITO', 'MOGADOURO', 'TRANCOSO', 'VIANA DO CASTELO', 'ALJUSTREL',
    'MIRANDA DO DOURO', 'VIZELA', 'AVIS', 'BAIÃO', 'MÉRTOLA', 'ÓBIDOS', 'MONTIJO',
    'BATALHA', 'AZAMBUJA', 'ARRAIOLOS', 'GRÂNDOLA', 'SANTA MARTA DE PENAGUIÃO',
    'CELORICO DE BASTO', 'RIBEIRA DE PENA', 'PESO DA RÉGUA', 'MONDIM DE BASTO',
    'MONTEMOR-O-VELHO', 'MURÇA', 'CASTELO DE PAIVA', 'MURTOSA', 'MIRA',
    'PAMPILHOSA DA SERRA', 'VIDIGUEIRA', 'VILA NOVA DE FOZ CÔA', 'ESPINHO',
    'SERPA', 'MORTÁGUA', 'FIGUEIRÓ DOS VINHOS', 'PONTE DE SOR', 'PORTEL',
    'CAMPO MAIOR', 'MIRANDELA', 'FERREIRA DO ALENTEJO', 'ESPOSENDE',
    'ARRUDA DOS VINHOS', 'TAROUCA', 'MONFORTE', 'SOBRAL DE MONTE AGRAÇO',
    'SABROSA', 'OLIVEIRA DE FRADES', 'PROENÇA-A-NOVA', 'MOURA', 'SANTA COMBA DÃO',
    'ALIJÓ', 'ALMODÔVAR', 'BOTICAS', 'VILA DE REI', 'ALTER DO CHÃO', 'SERNANCELHE',
    'MANGUALDE', 'REDONDO', 'VILA NOVA DE CERVEIRA', 'ARRONCHES', 'OURIQUE',
    'TERRAS DE BOURO', 'NAZARÉ', 'VINHAIS', 'CARRAZEDA DE ANSIÃES', 'MESÃO FRIO',
    'BARRANCOS', 'VIANA DO ALENTEJO', 'CASTANHEIRA DE PÊRA', 'ALCOUTIM',
    'VILA VIÇOSA', 'GAVIÃO', 'CRATO', 'VIMIOSO', 'MORA', 'GÓIS', 'FRONTEIRA',
    'AGUIAR DA BEIRA', 'MARVÃO', 'ALANDROAL'],
  }},
  mounted() {
    // Initialize the Leaflet map
    var map = L.map('map').setView([40.000, -8.000], 6);
    // Add the OpenStreetMap tile layer
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data &copy; <a href="http://www.openstreetmap.org/">OpenStreetMap</a> contributors',
      maxZoom: 18,
    }).addTo(map);

    const that = this;

    // Add a click event listener to the map
    map.on('click', function(e) {
      // Get the latitude and longitude of the clicked point
      const lat = e.latlng.lat.toFixed(4);
      const lon = e.latlng.lng.toFixed(4);
      that.getPlace(lat, lon);
    });
  },
  methods: {
    async getPlace(lat, lon) {
      try {
        const response = await fetch(`http://chifrolas.com/api/get_location?lat=${lat}&lon=${lon}`);
        const res = await response.json();
        console.log(res);
        this.selected_distrito = res.district ? res.district.toUpperCase() : null;
        this.selected_concelho = res.municipality ? res.municipality.toUpperCase() : null;
      } catch (e) {
        alert("Ocorreu um erro, verifique o console");
        console.log(e);
      }
    },
    async getHh() {
      try {
        this.awaitingState = 1;
        const response = await fetch(`http://chifrolas.com/api/predict?municipality=${this.selected_concelho}&issue=${this.selected_occurence_type}`);
        const res = await response.json();
        console.log(res);
        this.hora_homem = res.hh;
        this.greatestRisk = res.risk_issue;
        this.awaitingState = 2;
      } catch (e) {
        alert("Ocorreu um erro, verifique o console");
        console.log(e);
      }
    },
    tryAgain() {
      this.awaitingState = 0;
      this.selected_occurence_type = null;
      this.selected_distrito = null;
      this.selected_concelho = null;
      this.hora_homem = 0;
      this.greatestRisk = '';
      this.awaitingState = 0; // 0 - not begun, 1 - waiting, 2 - done
    },
  },
}
</script>

<style>
  li { margin: 6px 0; }
</style>
