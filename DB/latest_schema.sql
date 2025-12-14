--
-- PostgreSQL database dump
--

\restrict Nc1AdOscadetOltKztQBP9gY0uckGbQsrVSUUAQJKX42zySI2ie1erNEg1dbOzh

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.performances DROP CONSTRAINT IF EXISTS fk_performances_ensemble_id_ensembles;
ALTER TABLE IF EXISTS ONLY public.performances DROP CONSTRAINT IF EXISTS fk_performances_composition_id_compositions;
ALTER TABLE IF EXISTS ONLY public.performance_record DROP CONSTRAINT IF EXISTS fk_performance_record_record_id_records;
ALTER TABLE IF EXISTS ONLY public.performance_record DROP CONSTRAINT IF EXISTS fk_performance_record_performance_id_performances;
ALTER TABLE IF EXISTS ONLY public.musician_ensemble DROP CONSTRAINT IF EXISTS fk_musician_ensemble_musician_id_musicians;
ALTER TABLE IF EXISTS ONLY public.musician_ensemble DROP CONSTRAINT IF EXISTS fk_musician_ensemble_ensemble_id_ensembles;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS uq_users_username;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS uq_users_email;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS pk_users;
ALTER TABLE IF EXISTS ONLY public.records DROP CONSTRAINT IF EXISTS pk_records;
ALTER TABLE IF EXISTS ONLY public.performances DROP CONSTRAINT IF EXISTS pk_performances;
ALTER TABLE IF EXISTS ONLY public.musicians DROP CONSTRAINT IF EXISTS pk_musicians;
ALTER TABLE IF EXISTS ONLY public.ensembles DROP CONSTRAINT IF EXISTS pk_ensembles;
ALTER TABLE IF EXISTS ONLY public.compositions DROP CONSTRAINT IF EXISTS pk_compositions;
ALTER TABLE IF EXISTS ONLY public.alembic_version DROP CONSTRAINT IF EXISTS alembic_version_pkc;
ALTER TABLE IF EXISTS public.users ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.records ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.performances ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.musicians ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.ensembles ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.compositions ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.users_id_seq;
DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.records_id_seq;
DROP TABLE IF EXISTS public.records;
DROP SEQUENCE IF EXISTS public.performances_id_seq;
DROP TABLE IF EXISTS public.performances;
DROP TABLE IF EXISTS public.performance_record;
DROP SEQUENCE IF EXISTS public.musicians_id_seq;
DROP TABLE IF EXISTS public.musicians;
DROP TABLE IF EXISTS public.musician_ensemble;
DROP SEQUENCE IF EXISTS public.ensembles_id_seq;
DROP TABLE IF EXISTS public.ensembles;
DROP SEQUENCE IF EXISTS public.compositions_id_seq;
DROP TABLE IF EXISTS public.compositions;
DROP TABLE IF EXISTS public.alembic_version;
DROP TYPE IF EXISTS public.musiciantype;
DROP TYPE IF EXISTS public.ensembletype;
--
-- Name: ensembletype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.ensembletype AS ENUM (
    'orchestra',
    'quartet',
    'quintet'
);


--
-- Name: musiciantype; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.musiciantype AS ENUM (
    'performer',
    'composer',
    'conductor',
    'director'
);


SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: compositions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.compositions (
    name character varying(100) NOT NULL,
    about character varying(1000),
    id integer NOT NULL
);


--
-- Name: compositions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.compositions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: compositions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.compositions_id_seq OWNED BY public.compositions.id;


--
-- Name: ensembles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ensembles (
    name character varying(100) NOT NULL,
    about character varying(1000),
    ensemble_type public.ensembletype NOT NULL,
    id integer NOT NULL
);


--
-- Name: ensembles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ensembles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ensembles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ensembles_id_seq OWNED BY public.ensembles.id;


--
-- Name: musician_ensemble; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.musician_ensemble (
    musician_id integer,
    ensemble_id integer
);


--
-- Name: musicians; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.musicians (
    name character varying(100) NOT NULL,
    about character varying(1000),
    musician_type public.musiciantype NOT NULL,
    id integer NOT NULL
);


--
-- Name: musicians_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.musicians_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: musicians_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.musicians_id_seq OWNED BY public.musicians.id;


--
-- Name: performance_record; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.performance_record (
    performance_id integer,
    record_id integer
);


--
-- Name: performances; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.performances (
    performance_date date NOT NULL,
    composition_id integer NOT NULL,
    id integer NOT NULL,
    ensemble_id integer NOT NULL
);


--
-- Name: performances_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.performances_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: performances_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.performances_id_seq OWNED BY public.performances.id;


--
-- Name: records; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.records (
    company character varying(100) NOT NULL,
    wholesale_company_address character varying(100) NOT NULL,
    retail_price double precision NOT NULL,
    wholesale_price double precision NOT NULL,
    release_date date NOT NULL,
    current_year_sold integer NOT NULL,
    last_year_sold integer NOT NULL,
    remaining_stock integer NOT NULL,
    id integer NOT NULL
);


--
-- Name: records_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.records_id_seq OWNED BY public.records.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    username character varying NOT NULL,
    password_hash character varying(256) NOT NULL,
    email character varying NOT NULL,
    id integer NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: compositions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compositions ALTER COLUMN id SET DEFAULT nextval('public.compositions_id_seq'::regclass);


--
-- Name: ensembles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ensembles ALTER COLUMN id SET DEFAULT nextval('public.ensembles_id_seq'::regclass);


--
-- Name: musicians id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.musicians ALTER COLUMN id SET DEFAULT nextval('public.musicians_id_seq'::regclass);


--
-- Name: performances id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.performances ALTER COLUMN id SET DEFAULT nextval('public.performances_id_seq'::regclass);


--
-- Name: records id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.records ALTER COLUMN id SET DEFAULT nextval('public.records_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: compositions pk_compositions; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.compositions
    ADD CONSTRAINT pk_compositions PRIMARY KEY (id);


--
-- Name: ensembles pk_ensembles; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ensembles
    ADD CONSTRAINT pk_ensembles PRIMARY KEY (id);


--
-- Name: musicians pk_musicians; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.musicians
    ADD CONSTRAINT pk_musicians PRIMARY KEY (id);


--
-- Name: performances pk_performances; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.performances
    ADD CONSTRAINT pk_performances PRIMARY KEY (id);


--
-- Name: records pk_records; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.records
    ADD CONSTRAINT pk_records PRIMARY KEY (id);


--
-- Name: users pk_users; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT pk_users PRIMARY KEY (id);


--
-- Name: users uq_users_email; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT uq_users_email UNIQUE (email);


--
-- Name: users uq_users_username; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT uq_users_username UNIQUE (username);


--
-- Name: musician_ensemble fk_musician_ensemble_ensemble_id_ensembles; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.musician_ensemble
    ADD CONSTRAINT fk_musician_ensemble_ensemble_id_ensembles FOREIGN KEY (ensemble_id) REFERENCES public.ensembles(id) ON DELETE CASCADE;


--
-- Name: musician_ensemble fk_musician_ensemble_musician_id_musicians; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.musician_ensemble
    ADD CONSTRAINT fk_musician_ensemble_musician_id_musicians FOREIGN KEY (musician_id) REFERENCES public.musicians(id) ON DELETE CASCADE;


--
-- Name: performance_record fk_performance_record_performance_id_performances; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.performance_record
    ADD CONSTRAINT fk_performance_record_performance_id_performances FOREIGN KEY (performance_id) REFERENCES public.performances(id) ON DELETE CASCADE;


--
-- Name: performance_record fk_performance_record_record_id_records; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.performance_record
    ADD CONSTRAINT fk_performance_record_record_id_records FOREIGN KEY (record_id) REFERENCES public.records(id) ON DELETE CASCADE;


--
-- Name: performances fk_performances_composition_id_compositions; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.performances
    ADD CONSTRAINT fk_performances_composition_id_compositions FOREIGN KEY (composition_id) REFERENCES public.compositions(id) ON DELETE CASCADE;


--
-- Name: performances fk_performances_ensemble_id_ensembles; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.performances
    ADD CONSTRAINT fk_performances_ensemble_id_ensembles FOREIGN KEY (ensemble_id) REFERENCES public.ensembles(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict Nc1AdOscadetOltKztQBP9gY0uckGbQsrVSUUAQJKX42zySI2ie1erNEg1dbOzh

